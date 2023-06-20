$(document).ready(function(){
    $('a[data-link]').click(function(e){
      e.preventDefault();
      $.get($(this).attr('href'), function(response){
        setTimeout(function() {
          $('body').html(response);
        }, 200);  // задержка в 200 миллисекунд
      });
    });
  });
  