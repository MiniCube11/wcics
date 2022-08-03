var nav = document.getElementsByTagName('nav')[0];
var hamburger = document.getElementsByClassName('hamburger')[0];
var prevScrollPos = window.pageYOffset;
var emailLink = document.getElementById('email');

const toggleNav = () => {
    if (nav.classList.contains('nav-active')) return;
    var currentScrollPos = window.pageYOffset;
    if (currentScrollPos < 20) {
        nav.classList.add('nav-transparent');
    } else {
        nav.classList.remove('nav-transparent');
        if (prevScrollPos > currentScrollPos) {
            nav.classList.remove('nav-hide');
        } else {
            nav.classList.add('nav-hide');
        }
    }
    prevScrollPos = currentScrollPos;
};

const toggleHamburger = () => {
    if (nav.classList.contains('nav-active')) {
        nav.classList.remove('nav-active');
        toggleNav();
    } else {
        nav.classList.add('nav-active');
        nav.classList.remove('nav-transparent');
    }
};

const toggleEmails = () => {
    var contactEmails = document.getElementsByClassName('contact-emails')[0];
    contactEmails.classList.toggle('contact-emails-active');
}

hamburger.onclick = toggleHamburger;
window.onscroll = toggleNav;
emailLink.onclick = toggleEmails;