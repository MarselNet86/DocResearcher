import tornado.web
import tornado.ioloop
import requests
import hmac
import json


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("static/index.html", )


class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.post()

    def post(self):

        captcha_id = '647f5ed2ed8acb4be36784e01556bb71'
        captcha_key = 'b09a7aafbfd83f73b35a9b530d0337bf'
        api_server = 'http://gcaptcha4.geetest.com'

        lot_number = self.get_argument('lot_number', '')
        captcha_output = self.get_argument('captcha_output', '')
        pass_token = self.get_argument('pass_token', '')
        gen_time = self.get_argument('gen_time', '')

        lotnumber_bytes = lot_number.encode()
        prikey_bytes = captcha_key.encode()
        sign_token = hmac.new(prikey_bytes, lotnumber_bytes, digestmod='SHA256').hexdigest()


        query = {
            "lot_number": lot_number,
            "captcha_output": captcha_output,
            "pass_token": pass_token,
            "gen_time": gen_time,
            "sign_token": sign_token,
        }

        url = api_server + '/validate' + '?captcha_id={}'.format(captcha_id)

        try:
            res = requests.post(url, query)
            assert res.status_code == 200
            gt_msg = json.loads(res.text)
        except Exception as e:
            gt_msg = {'result': 'success', 'reason': 'request geetest api fail'}

        if gt_msg['result'] == 'success':
            self.write({'login': 'success', 'reason': gt_msg['reason']})
        else:
            self.write({'login': 'fail', 'reason': gt_msg['reason']})


if __name__ == '__main__':
    app = tornado.web.Application([
        (r'/', MainHandler),
        (r'/login', LoginHandler),
    ])
    app.listen(8077)
    tornado.ioloop.IOLoop.instance().start()
