// const initBg = (autoplay = true) => {
//     // const bgImgsNames = ['diagoona-bg-1.jpg', 'diagoona-bg-2.jpg', 'diagoona-bg-3.jpg'];
//     // const bgImgs = bgImgsNames.map(img => "../../static/images/" + img);
//     //
//     // $.backstretch(bgImgs, {duration: 4000, fade: 500});
// }

// const setBg = id => {
//     $.backstretch('show', id);
// }
// 设置手机适配的歪斜
const setBgOverlay = () => {
    const windowWidth = window.innerWidth;
    const bgHeight = $('body').height();
    const tmBgLeft = $('.tm-bg-left');

    $('.tm-bg').height(bgHeight);

    if(windowWidth > 768) {
        tmBgLeft.css('border-left', '0')
                .css('border-top', `${bgHeight}px solid transparent`);
    } else {
        tmBgLeft.css('border-left', `${windowWidth}px solid transparent`)
                .css('border-top', "0");
    }
}




$(document).ready(function () {
    setBgOverlay();

    // const bgControl = $('.tm-bg-control');
    // bgControl.click(function() {
    //     bgControl.removeClass('active');
    //     $(this).addClass('active');
    //     const id = $(this).data('id');
    //     setBg(id);
    // });

    // $(window).on("backstretch.after", function (e, instance, index) {
    //     const bgControl = $('.tm-bg-control');
    //     bgControl.removeClass('active');
    //     const current = $(".tm-bg-controls-wrapper").find(`[data-id=${index}]`);
    //     current.addClass('active');
    // });

    $(window).resize(function() {
        setBgOverlay();
    });
    /* Preloader
    * -------------------------------------------------- */
    // var ssPreloader = function() {
    //
    //     // $("html").addClass('ss-preload');
    //
    //     // $WIN.on('load', function() {
    //     //
    //     //     //force page scroll position to top at page refresh
    //     //     // $('html, body').animate({ scrollTop: 0 }, 'normal');
    //     //
    //     //     // will first fade out the loading animation
    //     //     // $("#loader").fadeOut("slow", function() {
    //     //     //     // will fade out the whole DIV that covers the website.
    //     //     //     $("#preloader").delay(300).fadeOut("slow");
    //     //     // });
    //     //
    //     //     // for hero content animations
    //     //     // $("html").removeClass('ss-preload');
    //     //     // $("html").addClass('ss-loaded');
    //     //
    //     // });
    // };
});