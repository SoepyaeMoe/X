export function initializeAuthForm() {
    const loginBtn = document.querySelectorAll(".login-btn");
    const registerBtn = document.querySelectorAll(".register-btn");
    const closeBtn = document.querySelectorAll(".close-btn");

    loginBtn.forEach(e => {
        e.addEventListener("click", () => {
            document.querySelector("#login-form").style.display = 'flex';
            document.querySelector("#register-form").style.display = 'none';
        });
    });

    registerBtn.forEach(e => {
        e.addEventListener("click", () => {
            document.querySelector("#register-form").style.display = 'flex';
            document.querySelector("#login-form").style.display = 'none';
        });
    });

    closeBtn.forEach(e => {
        e.addEventListener("click", () => {
            document.querySelector("#login-form").style.display = 'none';
            document.querySelector("#register-form").style.display = 'none';
        });
    });
}


let currentScrollY = window.scrollY;
window.onscroll = () => {
    if (currentScrollY > window.scrollY) {
        if (window.scrollY == 0) {
            document.querySelector('.mobile-nav').style.top = '-100%';

            // document.querySelector('.mobile-bottom-nav').style.bottom = '-100%';
        } else {
            document.querySelector('.mobile-nav').style.top = '0';
            document.querySelector('.mobile-bottom-nav').style.bottom = '0';
        }
    } else {
        document.querySelector('.mobile-nav').style.top = '-100%';
        document.querySelector('.mobile-bottom-nav').style.bottom = '-100%';
    }
    currentScrollY = window.scrollY
}
