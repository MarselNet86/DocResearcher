const goTopBtn = document.querySelector(".go-top");

const goTop = () => {
    if (window.scrollY > 0) {
        window.scrollBy(0, -75);
        setTimeout(goTop, 0);
    }
}

goTopBtn.addEventListener("click", goTop);
