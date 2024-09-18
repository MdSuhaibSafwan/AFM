
jQuery(document).ready(function($) {
	var svg = '<img src="https://tag-afm-bucket.s3.amazonaws.com/static/assets/AFM-Student-guideline.png" loading="lazy" alt="Student guideline" title="Student guideline" height="" width="">';

	$(".svg-container").append(svg);

	$(window).scroll(function() {
        if($("body").hasClass("afm-how-work")) {
            const spaceHolder = document.querySelector('.timeline');
            const horizontal = document.querySelector('.timeline > div > div');
            spaceHolder.style.height = `${calcDynamicHeight(horizontal)}px`;

            function calcDynamicHeight(ref) {
                const vw = window.innerWidth;
                const vh = window.innerHeight + 350;
                const objectWidth = parseFloat(ref.scrollWidth);
                return parseFloat(objectWidth - vw + vh);
            }

            var start = 2; 
            var end = 4205;
            var journey = end - start;

            window.addEventListener('scroll', () => {
                const sticky = document.querySelector('.timeline > div');
                const bar = document.getElementById('grp-current');
                var extra = parseFloat((sticky.offsetTop / 4069) * 135); // calcuation for missing distance from the finish line
                horizontal.style.transform = `translateX(-${sticky.offsetTop}px)`;
                
                // convert to svg coodrinate system                
                var status = sticky.offsetTop;
                var max = horizontal.scrollWidth - window.innerWidth;
                var percentage = status / max;

                var tl_bar = (journey * percentage) + start;  

                $('#grp-current').attr('x', tl_bar);

               
            });

            window.addEventListener('resize', () => {
                spaceHolder.style.height = `${calcDynamicHeight(horizontal)}px`;
            });

            
        }
    });

    $(".svg-container2").append(svg);

    $(window).scroll(function() {
        if($("body").hasClass("afm-how-work")) {
            const spaceHolder = document.querySelector('.timeline2');
            const horizontal = document.querySelector('.timeline2 > div > div');
            spaceHolder.style.height = `${calcDynamicHeight(horizontal)}px`;

            function calcDynamicHeight(ref) {
                const vw = window.innerWidth;
                const vh = window.innerHeight + 350;
                const objectWidth = parseFloat(ref.scrollWidth);
                return parseFloat(objectWidth - vw + vh);
            }

            var start = 2; 
            var end = 4205;
            var journey = end - start;

            window.addEventListener('scroll', () => {
                const sticky = document.querySelector('.timeline2 > div');
                const bar = document.getElementById('grp-current');
                var extra = parseFloat((sticky.offsetTop / 4069) * 135); // calcuation for missing distance from the finish line
                horizontal.style.transform = `translateX(-${sticky.offsetTop}px)`;
                
                // convert to svg coodrinate system                
                var status = sticky.offsetTop;
                var max = horizontal.scrollWidth - window.innerWidth;
                var percentage = status / max;

                var tl_bar = (journey * percentage) + start;  

                $('#grp-current').attr('x', tl_bar);

            });

            window.addEventListener('resize', () => {
                spaceHolder.style.height = `${calcDynamicHeight(horizontal)}px`;
            });

            /*
            // getting the length of the svg path
            const svg = document.getElementById("svgPath");
            const length = svg.getTotalLength();

            // start position of the drawing - normal display pre-animation
            svg.style.strokeDasharray = length;

            // hides the svg before the scrolling starts
            svg.style.strokeDashoffset = length;

            // offset the svg dash by the same amount as the percentage scrolled
            window.addEventListener("scroll", function () {
              const scrollpercent = (document.body.scrollTop + document.documentElement.scrollTop) / (document.documentElement.scrollHeight - document.documentElement.clientHeight);

              const draw = length * scrollpercent;

              // Reverse the drawing (when scrolling upwards)
              svg.style.strokeDashoffset = length - draw;

            });
            */
        }
    });
});
