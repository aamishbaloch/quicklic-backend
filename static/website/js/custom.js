/*=========================================================================
        Preloader
=========================================================================*/
$(window).load(function() {
    "use strict";
    $(".preloader-outer").delay(350).fadeOut('slow');
});

$(function(){
    "use strict";
    /*=========================================================================
            One Page Nav
    =========================================================================*/
    $('.navbar-default').singlePageNav({
        offset: $('.navbar-default').outerHeight(),
        filter: ':not(.external)',
        updateHash: false,
        speed: 1500,
        easing: 'swing'
    });

    /*=========================================================================
            Navigation Bar 2 Hamburger Menu
    =========================================================================*/
    $(".navicon-wrap").on( 'click', function() {
        $(".navicon").toggleClass("expanded");
        $('#slide-menu').toggleClass('expanded')
    });

    /*=========================================================================
            Facts Counter
    =========================================================================*/
    $('.counter').counterUp({
        delay: 5,
        time: 3000
    });

    /*=========================================================================
            Mailchimp Integration
    =========================================================================*/
    $('#mailchimp, #mailchimp-single, #mailchimp-footer').ajaxChimp({
      callback: function(response) {
        $('#mailchimp .result, #mailchimp-single .result, #mailchimp-footer .result').text(response.msg);
      }
    });

    /*=========================================================================
            Slick Slider
    =========================================================================*/
    $( ".slick-dots" ).appendTo( "#showcase-dots" );

    $('.reviews-slide').slick({
        dots: true,
        arrows: false,
        responsive: [
          {
            breakpoint: 768,
            settings: {
              arrows: false
            }
          }
        ]
      });

    $('.reviews-slide-2').slick({
      slidesToShow: 1,
      slidesToScroll: 1,
      arrows: false,
      fade: true,
      asNavFor: '.reviews-nav'
    });
    $('.reviews-nav').slick({
      slidesToShow: 3,
      slidesToScroll: 1,
      asNavFor: '.reviews-slide-2',
      dots: true,
      centerMode: true,
      focusOnSelect: true
    });

    $('.screenshots-01-wrap').slick({
      infinite: true,
      arrows: false,
      dots: true,
      slidesToShow: 4,
      slidesToScroll: 4,
      autoplay: true,
      autoplaySpeed: 2000,
      speed: 2000,
      responsive: [
        {
          breakpoint: 1921,
          settings: {
            slidesToShow: 4,
            slidesToScroll: 4
          }
        },
        {
          breakpoint: 1441,
          settings: {
            slidesToShow: 4,
            slidesToScroll: 4
          }
        },
        {
          breakpoint: 1281,
          settings: {
            slidesToShow: 4,
            slidesToScroll: 4
          }
        },
        {
          breakpoint: 768,
          settings: {
            slidesToShow: 3,
            slidesToScroll: 3
          }
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        }
      ]
    });

    $('.screenshots-02-wrap').slick({
      infinite: true,
      arrows: false,
      dots: true,
      slidesToShow: 4,
      slidesToScroll: 4,
      autoplay: true,
      autoplaySpeed: 2000,
      speed: 2000,
      responsive: [
        {
          breakpoint: 1921,
          settings: {
            slidesToShow: 6,
            slidesToScroll: 3
          }
        },
        {
          breakpoint: 1441,
          settings: {
            slidesToShow: 6,
            slidesToScroll: 3
          }
        },
        {
          breakpoint: 1281,
          settings: {
            slidesToShow: 4,
            slidesToScroll: 3
          }
        },
        {
          breakpoint: 768,
          settings: {
            slidesToShow: 3,
            slidesToScroll: 3
          }
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        }
      ]
    });

    $('.screenshots-03-wrap').slick({
      arrows: false,
      dots: true,
      centerMode: true,
      centerPadding: '0',
      slidesToShow: 5,
      autoplay: true,
      autoplaySpeed: 2000,
      speed: 1000,
      responsive: [
        {
          breakpoint: 1921,
          settings: {
            slidesToShow: 7,
            slidesToScroll: 3
          }
        },
        {
          breakpoint: 1441,
          settings: {
            slidesToShow: 5,
            slidesToScroll: 3
          }
        },
        {
          breakpoint: 1281,
          settings: {
            slidesToShow: 5,
            slidesToScroll: 3
          }
        },
        {
          breakpoint: 768,
          settings: {
            slidesToShow: 3,
            slidesToScroll: 3
          }
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        }
      ]
    });

    /*=========================================================================
            Scroll Reveal Animation Settings
    =========================================================================*/
    window.sr = ScrollReveal({ useDelay: 'once' });

    sr.reveal('.b20-1', { 
      origin: 'bottom',
      distance: '20px',
      duration: 1500,
      delay: 100,
      opacity: 0,
      scale: 1,
      reset: false,
    });

    sr.reveal('.b20-2', { 
      origin: 'bottom',
      distance: '20px',
      duration: 1500,
      delay: 200,
      opacity: 0,
      scale: 1,
      reset: false,
    });

    sr.reveal('.b20-3', { 
      origin: 'bottom',
      distance: '20px',
      duration: 1500,
      delay: 300,
      opacity: 0,
      scale: 1,
      reset: false,
    });

    sr.reveal('.b20-4', { 
      origin: 'bottom',
      distance: '20px',
      duration: 1500,
      delay: 400,
      opacity: 0,
      scale: 1,
      reset: false,
    });

    sr.reveal('.r30-1', { 
      origin: 'right',
      distance: '30px',
      duration: 2000,
      delay: 300,
      opacity: 0,
      scale: 1,
      reset: false,
    });

    sr.reveal('.b40-1', { 
      origin: 'bottom',
      distance: '40px',
      duration: 1500,
      delay: 100,
      opacity: 0,
      scale: 1,
      reset: false,
    });

    sr.reveal('.t40-1', { 
      origin: 'top',
      distance: '40px',
      duration: 1500,
      delay: 500,
      opacity: 0,
      scale: 1,
      useDelay: 'always',
      reset: true,
    });

    sr.reveal('.t40-2', { 
      origin: 'top',
      distance: '40px',
      duration: 1500,
      delay: 800,
      opacity: 0,
      scale: 1,
      useDelay: 'always',
      reset: true,
    });

    sr.reveal('.t40-3', { 
      origin: 'top',
      distance: '40px',
      duration: 1500,
      delay: 1100,
      opacity: 0,
      scale: 1,
      useDelay: 'always',
      reset: true,
    });

    sr.reveal('.l40-1', { 
      origin: 'left',
      distance: '40px',
      duration: 1500,
      delay: 100,
      opacity: 0,
      scale: 1,
      reset: false,
    });

    sr.reveal('.r40-1', { 
      origin: 'right',
      distance: '40px',
      duration: 1500,
      delay: 100,
      opacity: 0,
      scale: 1,
      reset: false,
    });

    sr.reveal('.s1-1', { 
      origin: 'bottom',
      distance: '0',
      duration: 400,
      delay: 600,
      scale: 1.5,
      reset: false,
    });

    sr.reveal('.s1-2', { 
      origin: 'bottom',
      distance: '0',
      duration: 400,
      delay: 1000,
      scale: 1.5,
      reset: false,
    });

    sr.reveal('.s1-3', { 
      origin: 'bottom',
      distance: '0',
      duration: 400,
      delay: 1400,
      scale: 1.5,
      reset: false,
    });

    /*=========================================================================
            Magnific Popup Functions
    =========================================================================*/
    $('.video-icon').magnificPopup({
      type: 'iframe',
      iframe: {
          markup: '<div class="mfp-iframe-scaler">'+
                    '<div class="mfp-close"></div>'+
                    '<iframe class="mfp-iframe" frameborder="0" allowfullscreen></iframe>'+
                  '</div>', 

          patterns: {
            youtube: {
              index: 'youtube.com/',

              id: 'v=',

              src: 'http://www.youtube.com/embed/%id%?autoplay=1'
            },
            vimeo: {
              index: 'vimeo.com/',
              id: '/',
              src: 'http://player.vimeo.com/video/%id%?autoplay=1'
            },
            gmaps: {
              index: '//maps.google.',
              src: '%id%&output=embed'
            }

          },

          srcAction: 'iframe_src',
        }
    });

});

/*=========================================================================
        Sticky Header Animation
=========================================================================*/
var animatedHeader = (function() {
  "use strict";

  var docElem = document.documentElement,
    header = document.querySelector( ".navbar-default" ),
    didScroll = false,
    changeHeaderOn = 100;

  function init() {
    window.addEventListener( 'scroll', function( event ) {
      if( !didScroll ) {
        didScroll = true;
        setTimeout( scrollPage, 250 );
      }
    }, false );
  }

  function scrollPage() {
    var sy = scrollY();
    if ( sy >= changeHeaderOn ) {
      classie.add( header, 'shrink' );
    }
    else {
      classie.remove( header, 'shrink' );
    }
    didScroll = false;
  }

  function scrollY() {
    return window.pageYOffset || docElem.scrollTop;
  }

  init();

})();