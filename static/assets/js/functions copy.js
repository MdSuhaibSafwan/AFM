var AFM = {}, $ = jQuery.noConflict();
!function (e) {
    var a = e(window), t = e("body"), n = (e(".body-inner"), e("section")), i = e("#topbar"), s = e("#header"),
        o = s.attr("class"), r = e("#logo"), l = e("#mainMenu"), d = e("#mainMenu-trigger a, #mainMenu-trigger button");
    if (e("#slider"), e(".AFM-slider"), e(".carousel"), e(".grid-layout"), e(".grid-filter, .page-grid-filter"), a.width(), s.length > 0) var c = s.offset().top;
    var u = {
        isMobile: function () {
            return !!navigator.userAgent.match(/(iPhone|iPod|iPad|Android|BlackBerry)/)
        },
        submenuLight: 1 == s.hasClass("submenu-light"),
        headerHasDarkClass: 1 == s.hasClass("dark"),
        headerDarkClassRemoved: !1,
        sliderDarkClass: !1,
        menuIsOpen: !1,
        menuOverlayOpened: !1
    };
    e(window).breakpoints({
        triggerOnInit: !0,
        breakpoints: [{name: "xs", width: 0}, {name: "sm", width: 576}, {name: "md", width: 768}, {
            name: "lg",
            width: 1025
        }, {name: "xl", width: 1200}]
    });
    var p = e(window).breakpoints("getBreakpoint");
    t.addClass("breakpoint-" + p), e(window).bind("breakpoint-change", function (e) {
        t.removeClass("breakpoint-" + e.from), t.addClass("breakpoint-" + e.to)
    }), e(window).bind("breakpoint-change", function (a) {
        e(window).breakpoints("greaterEqualTo", "lg", function () {
            t.addClass("b--desktop"), t.removeClass("b--responsive")
        }), e(window).breakpoints("lessThan", "lg", function () {
            t.removeClass("b--desktop"), t.addClass("b--responsive")
        })
    }), AFM.core = {
        functions: function () {
            AFM.core.scrollTop(), AFM.core.rtlStatus(), AFM.core.equalize(), AFM.core.customHeight()
        }, scrollTop: function () {
            var n = e("#scrollTop");
            if (n.length > 0) {
                var i = t.attr("data-offset") || 400;
                a.scrollTop() > i ? t.hasClass("frame") ? n.css({
                    bottom: "46px",
                    opacity: 1,
                    "z-index": 199
                }) : n.css({bottom: "26px", opacity: 1, "z-index": 199}) : n.css({
                    bottom: "16px",
                    opacity: 0
                }), n.off("click").on("click", function () {
                    return e("body,html").stop(!0).animate({scrollTop: 0}, 1e3, "easeInOutExpo"), !1
                })
            }
        }, rtlStatus: function () {
            return "rtl" == e("html").attr("dir")
        }, equalize: function () {
            var a = e(".equalize");
            a.length > 0 && a.each(function () {
                var a = e(this), t = a.find(a.attr("data-equalize-item")) || "> div", n = 0;
                t.each(function () {
                    e(this).outerHeight(!0) > n && (n = e(this).outerHeight(!0))
                }), t.height(n)
            })
        }, customHeight: function (a) {
            var t = e(".custom-height");
            t.length > 0 && t.each(function () {
                var t = e(this), n = t.attr("data-height") || 400, i = t.attr("data-height-lg") || n,
                    s = t.attr("data-height-md") || i, o = t.attr("data-height-sm") || s,
                    r = t.attr("data-height-xs") || o;

                function l(a) {
                    switch (a && (t = a), e(window).breakpoints("getBreakpoint")) {
                        case"xs":
                            t.height(r);
                            break;
                        case"sm":
                            t.height(o);
                            break;
                        case"md":
                            t.height(s);
                            break;
                        case"lg":
                            t.height(i);
                            break;
                        case"xl":
                            t.height(n)
                    }
                }

                l(a), e(window).resize(function () {
                    setTimeout(function () {
                        l(a)
                    }, 100)
                })
            })
        }
    }, AFM.header = {
        functions: function () {
            AFM.header.logoStatus(), AFM.header.stickyHeader(), AFM.header.topBar(), AFM.header.mainMenu(), AFM.header.mainMenuOverlay(), AFM.header.pageMenu(), AFM.header.sidebarOverlay(), AFM.header.dotsMenu(), AFM.header.onepageMenu()
        }, logoStatus: function (a) {
            var t = r.find(e(".logo-default")), n = r.find(e(".logo-dark")), i = r.find(".logo-fixed"),
                o = r.find(".logo-responsive");
            s.hasClass("header-sticky") && i.length > 0 ? (t.css("display", "none"), n.css("display", "none"), o.css("display", "none")) : (t.removeAttr("style"), n.removeAttr("style"), o.removeAttr("style"), i.removeAttr("style")), e(window).breakpoints("lessThan", "lg", function () {
                o.length > 0 && (t.css("display", "none"), n.css("display", "none"), i.css("display", "none"), o.css("display", "block"))
            })
        }, stickyHeader: function () {
            var n = s.attr("data-shrink") || 0, i = s.attr("data-sticky-active") || 200, r = a.scrollTop();
            s.hasClass("header-modern") && (n = 300), e(window).breakpoints("greaterEqualTo", "lg", function () {
                s.is(".header-disable-fixed") || (r > c + n ? (s.addClass("header-sticky"), r > c + i && (s.addClass("sticky-active"), u.submenuLight && u.headerHasDarkClass && (s.removeClass("dark"), u.headerDarkClassRemoved = !0), AFM.header.logoStatus())) : (s.removeClass().addClass(o), u.sliderDarkClass && u.headerHasDarkClass && (s.removeClass("dark"), u.headerDarkClassRemoved = !0), AFM.header.logoStatus()))
            }), e(window).breakpoints("lessThan", "lg", function () {
                "true" == s.attr("data-responsive-fixed") && (r > c + n ? (s.addClass("header-sticky"), r > c + i && (s.addClass("sticky-active"), u.submenuLight && (s.removeClass("dark"), u.headerDarkClassRemoved = !0), AFM.header.logoStatus())) : (s.removeClass().addClass(o), 1 == u.headerDarkClassRemoved && t.hasClass("mainMenu-open") && s.removeClass("dark"), AFM.header.logoStatus()))
            })
        }, topBar: function () {
            i.length > 0 && e("#topbar .topbar-dropdown .topbar-form").each(function (t, n) {
                a.width() - (e(n).width() + e(n).offset().left) < 0 && e(n).addClass("dropdown-invert")
            })
        }, mainMenu: function () {
            if (l.length > 0) {
                l.find(".dropdown, .dropdown-submenu");
                var n = e('#mainMenu nav > ul > li.dropdown > a[href="#"], #mainMenu nav > ul > li.dropdown > .dropdown-arrow, .dropdown-submenu > a[href="#"], .dropdown-submenu > .dropdown-arrow, .dropdown-submenu > span, .page-menu nav > ul > li.dropdown > a'),
                    i = e("#mainMenu-trigger a, #mainMenu-trigger button"), o = !1;
                i.on("click", function (n) {
                    var i = e(this);
                    n.preventDefault(), e(window).breakpoints("lessThan", "lg", function () {
                        u.menuIsOpen ? o || (o = !0, u.menuIsOpen = !1, AFM.header.logoStatus(), l.animate({"min-height": 0}, {
                            start: function () {
                                l.removeClass("menu-animate")
                            }, done: function () {
                                t.removeClass("mainMenu-open"), i.removeClass("toggle-active"), u.submenuLight && u.headerHasDarkClass && u.headerDarkClassRemoved && !s.hasClass("header-sticky") && s.addClass("dark"), u.sliderDarkClass && u.headerHasDarkClass && u.headerDarkClassRemoved && (s.removeClass("dark"), u.headerDarkClassRemoved = !0)
                            }, duration: 500, easing: "easeInOutQuart", complete: function () {
                                o = !1
                            }
                        })) : o || (o = !0, u.menuIsOpen = !0, u.submenuLight && u.headerHasDarkClass ? (s.removeClass("dark"), u.headerDarkClassRemoved = !0) : u.headerHasDarkClass && u.headerDarkClassRemoved && s.addClass("dark"), i.addClass("toggle-active"), t.addClass("mainMenu-open"), AFM.header.logoStatus(), l.animate({"min-height": a.height()}, {
                            duration: 500,
                            easing: "easeInOutQuart",
                            start: function () {
                                setTimeout(function () {
                                    l.addClass("menu-animate")
                                }, 300)
                            },
                            complete: function () {
                                o = !1
                            }
                        }))
                    })
                }), n.on("click", function (a) {
                    e(this).parent("li").siblings().removeClass("hover-active"), (t.hasClass("b--responsive") || l.hasClass("menu-onclick")) && e(this).parent("li").toggleClass("hover-active"), a.stopPropagation(), a.preventDefault()
                }), t.on("click", function (e) {
                    l.find(".hover-active").removeClass("hover-active")
                }), e(window).on("resize", function () {
                    t.hasClass("mainMenu-open") && u.menuIsOpen && (d.trigger("click"), l.find(".hover-active").removeClass("hover-active"))
                }), e(window).breakpoints("greaterEqualTo", "lg", function () {
                    var t = e("nav > ul > li:last-child"), n = e("nav > ul > li:last-child > ul"),
                        i = (n.width(), t.width(), e("nav > ul > li").find(".dropdown-menu"));
                    i.css("display", "block"), e(".dropdown:not(.mega-menu-item) ul ul").each(function (t, n) {
                        a.width() - (e(n).width() + e(n).offset().left) < 0 && e(n).addClass("menu-invert")
                    }), n.length > 0 && a.width() - (n.width() + t.offset().left) < 0 && n.addClass("menu-last"), i.css("display", "")
                })
            }
        }, mainMenuOverlay: function () {
        }, pageMenu: function () {
            var t = e(".page-menu");
            t.length > 0 && (e(window).breakpoints("greaterEqualTo", "lg", function () {
                var e = t.attr("data-shrink") || t.offset().top + 200;
                "true" == t.attr("data-sticky") && a.scroll(function () {
                    a.scrollTop() > e ? (t.addClass("sticky-active"), s.addClass("pageMenu-sticky")) : (t.removeClass("sticky-active"), s.removeClass("pageMenu-sticky"))
                })
            }), t.each(function () {
                e(this).find("#pageMenu-trigger").on("click", function () {
                    t.toggleClass("page-menu-active"), t.toggleClass("items-visible")
                })
            }))
        }, sidebarOverlay: function () {
            var a = e("#side-panel");
            a.length > 0 && (a.css("opacity", 1), e("#close-panel").on("click", function () {
                t.removeClass("side-panel-active"), e("#side-panel-trigger").removeClass("toggle-active")
            }));
            var n = e("#sidepanel"), i = e(".panel-trigger"), s = !1;
            i.on("click", function (e) {
                e.preventDefault(), u.panelIsOpen ? s || (s = !0, u.panelIsOpen = !1, n.removeClass("panel-open"), s = !1) : s || (s = !0, u.panelIsOpen = !0, n.addClass("panel-open"), s = !1)
            })
        }, dotsMenu: function () {
            var a = e("#dotsMenu"), t = a.find("ul > li > a");
            a.length > 0 && (t.on("click", function () {
                return t.parent("li").removeClass("current"), e(this).parent("li").addClass("current"), !1
            }), t.parents("li").removeClass("current"), a.find('a[href="#' + AFM.header.currentSection() + '"]').parent("li").addClass("current"))
        }, onepageMenu: function () {
            l.hasClass("menu-one-page") && e(window).on("scroll", function () {
                var e = AFM.header.currentSection();
                l.find("nav > ul > li > a").parents("li").removeClass("current"), l.find('nav > ul > li > a[href="#' + e + '"]').parent("li").addClass("current")
            })
        }, currentSection: function () {
            var t = "body";
            return n.each(function () {
                var n = e(this), i = n.attr("id");
                n.offset().top - a.height() / 3 < a.scrollTop() && n.offset().top + n.height() - a.height() / 3 > a.scrollTop() && (t = i)
            }), t
        }
    }, AFM.elements = {
        functions: function () {
            AFM.elements.naTo(), AFM.elements.buttons(), AFM.elements.accordion(), AFM.elements.animations(), AFM.elements.progressBar(), AFM.elements.tooltip(), AFM.elements.popover(), AFM.elements.modal(), AFM.elements.forms(), AFM.elements.formValidation(), AFM.elements.formAjaxProcessing()
        }, forms: function () {
            var a = e(".show-hide-password");
            a.length > 0 && a.each(function () {
                var a = e(this), t = a.find(".input-group-append i"), n = a.children("input");
                a.find(".input-group-append i").css({cursor: "pointer"}), t.on("click", function (e) {
                    e.preventDefault(), "text" == a.children("input").attr("type") ? (n.attr("type", "password"), t.removeClass("icon-eye"), t.addClass("icon-eye-off")) : "password" == a.children("input").attr("type") && (n.attr("type", "text"), t.addClass("icon-eye"), t.removeClass("icon-eye-off"))
                })
            })
        }, formValidation: function () {
            var e = document.getElementsByClassName("needs-validation");
            Array.prototype.filter.call(e, function (e) {
                e.addEventListener("submit", function (a) {
                    !1 === e.checkValidity() && (a.preventDefault(), a.stopPropagation()), e.classList.add("was-validated")
                }, !1)
            })
        }, formAjaxProcessing: function () {
            var a = e(".widget-contact-form:not(.custom-js), .ajax-form:not(.custom-js)");
            a.length > 0 && a.each(function () {
                var a = e(this),
                    t = a.attr("data-success-message") || "We have <strong>successfully</strong> received your Message and will get Back to you as soon as possible.",
                    n = a.attr("data-success-page"), i = a.find("button#form-submit"), s = i.html();
                Array.prototype.filter.call(a, function (e) {
                    e.addEventListener("submit", function (a) {
                        return !1 === e[0].checkValidity() && (a.preventDefault(), a.stopPropagation()), e.classList.add("was-validated"), !1
                    }, !1)
                }), a.submit(function (o) {
                    o.preventDefault();
                    var r = e(this).attr("action"), l = e(this).attr("method"), d = e(this).serialize();
                    !1 === a[0].checkValidity() ? (o.stopPropagation(), a.addClass("was-validated")) : (e(a).removeClass("was-validated"), i.html('<i class="icon-loader fa-spin"> </i> Sending...'), e.ajax({
                        url: r,
                        type: l,
                        data: d,
                        success: function (o) {
                            "success" == o.response ? (a.find(".g-recaptcha").children("div").length > 0 && grecaptcha.reset(), i.html(s), n ? window.location.href = n : e.notify({message: t}, {
                                type: "success",
                                delay: a.attr("data-success-message-delay") || 2e4
                            })) : (e.notify({message: a.attr("data-error-message") || o.message}, {
                                type: "danger",
                                delay: a.attr("data-error-message-delay") || 2e4
                            }), setTimeout(function () {
                                i.html(s)
                            }, 1e3))
                        }
                    }))
                })
            })
        }, naTo: function () {
            e("a.scroll-to, #dotsMenu > ul > li > a, .menu-one-page nav > ul > li > a:not([data-lightbox])").on("click", function () {
                var a = 0, t = 0;
                e(window).breakpoints("lessThan", "lg", function () {
                    u.menuIsOpen && d.trigger("click"), !0 === s.attr("data-responsive-fixed") && (t = s.height())
                }), e(window).breakpoints("greaterEqualTo", "lg", function () {
                    s.length > 0 && (t = s.height())
                }), e(".dashboard").length > 0 && (a = 30);
                var n = e(this);
                return e("html, body").stop(!0, !1).animate({scrollTop: e(n.attr("href")).offset().top - (t + a)}, 1500, "easeInOutExpo"), !1
            })
        }, buttons: function () {
            e(".btn-slide[data-width]") && e(".btn.btn-slide[data-width]").each(function () {
                var a, t = e(this), n = t.attr("data-width");
                switch (!0) {
                    case t.hasClass("btn-lg"):
                        a = "60";
                        break;
                    case t.hasClass("btn-sm"):
                        a = "36";
                        break;
                    case t.hasClass("btn-xs"):
                        a = "28";
                        break;
                    default:
                        a = "48"
                }
                t.hover(function () {
                    e(this).css("width", n + "px")
                }, function () {
                    e(this).css("width", a + "px")
                })
            })
        }, accordion: function () {
            var a = e(".ac-item");
            a.length && (a.each(function () {
                var a = e(this);
                a.hasClass("ac-active") ? a.addClass("ac-active") : a.find(".ac-content").hide()
            }), e(".ac-title").on("click", function (a) {
                var t = e(this), n = t.parents(".ac-item"), i = n.parents(".accordion");
                return n.hasClass("ac-active") ? i.hasClass("toggle") ? (n.removeClass("ac-active"), t.next(".ac-content").slideUp()) : (i.find(".ac-item").removeClass("ac-active"), i.find(".ac-content").slideUp()) : (i.hasClass("toggle") || (i.find(".ac-item").removeClass("ac-active"), i.find(".ac-content").slideUp("fast")), n.addClass("ac-active"), t.next(".ac-content").slideToggle("fast")), a.preventDefault(), !1
            }))
        }, animations: function () {
            var a = e("[data-animate]");
            if (a.length > 0) {
                if ("undefined" == typeof Waypoint) return AFM.elements.notification("Warning", "jQuery Waypoint plugin is missing in plugins.js file.", "danger"), !0;
                a.each(function () {
                    var a = e(this);
                    a.addClass("animated"), a.options = {
                        animation: a.attr("data-animate") || "fadeIn",
                        delay: a.attr("data-animate-delay") || 200,
                        direction: ~a.attr("data-animate").indexOf("Out") ? "back" : "forward",
                        offsetX: a.attr("data-animate-offsetX") || 0,
                        offsetY: a.attr("data-animate-offsetY") || -100
                    }, "forward" == a.options.direction ? new Waypoint({
                        element: a, handler: function () {
                            setTimeout(function () {
                                a.addClass(a.options.animation + " visible")
                            }, a.options.delay), this.destroy()
                        }, offset: "100%"
                    }) : (a.addClass("visible"), a.on("click", function () {
                        return a.addClass(a.options.animation), !1
                    })), a.parents(".demo-play-animations").length && a.on("click", function () {
                        return a.removeClass(a.options.animation), setTimeout(function () {
                            a.addClass(a.options.animation)
                        }, 50), !1
                    })
                })
            }
        }, progressBar: function () {
            var a = e(".p-progress-bar") || e(".progress-bar");
            a.length > 0 && a.each(function (a, n) {
                var i = e(this), s = i.attr("data-percent") || "100", o = i.attr("data-delay") || "60",
                    r = i.attr("data-type") || "%";
                i.hasClass("progress-animated") || i.css({width: "0%"});
                var l = function () {
                    i.animate({width: s + "%"}, "easeInOutCirc").addClass("progress-animated"), i.delay(o).append('<span class="progress-type">' + r + '</span><span class="progress-number animated fadeIn">' + s + "</span>")
                };
                t.hasClass("breakpoint-lg") || t.hasClass("breakpoint-xl") ? new Waypoint({
                    element: e(n),
                    handler: function () {
                        setTimeout(function () {
                            l()
                        }, o), this.destroy()
                    },
                    offset: "100%"
                }) : l()
            })
        }, tooltip: function () {
            var a = e('[data-toggle="tooltip"]');
            if (a.length > 0) {
                if (void 0 === e.fn.tooltip) return AFM.elements.notification("Warning: jQuery tooltip plugin is missing in plugins.js file.", "warning"), !0;
                a.tooltip()
            }
        }, popover: function () {
            var a = e('[data-toggle="popover"]');
            if (a.length > 0) {
                if (void 0 === e.fn.popover) return AFM.elements.notification("Warning: jQuery popover plugin is missing in plugins.js file.", "warning"), !0;
                a.popover({container: "body", html: !0})
            }
        }, modal: function () {
            if (void 0 === e.fn.magnificPopup) return AFM.elements.notification("Warning", "jQuery magnificPopup plugin is missing in plugins.js file.", "danger"), !0;
            var a = e(".modal"), t = e(".modal-strip"), n = e(".btn-modal"), i = e(".modal-close"),
                s = e(".cookie-notify"), o = s.find(".modal-confirm, .mfp-close");
            a.length > 0 && a.each(function () {
                var a = e(this), t = a.attr("data-delay") || 3e3, n = a.attr("data-cookie-expire") || 365,
                    s = a.attr("data-cookie-name") || "cookieModalName2020_3", o = 1 == a.data("cookie-enabled");
                if (a.attr("data-delay-dismiss"), a.hasClass("modal-auto-open")) {
                    var r = e(this);
                    setTimeout(function () {
                        r.addClass("modal-active")
                    }, t)
                }
                a.find(i).click(function () {
                    return a.removeClass("modal-active"), !1
                }), a.hasClass("modal-auto-open") && (1 != o ? setTimeout(function () {
                    e.magnificPopup.open({
                        items: {src: a},
                        type: "inline",
                        closeBtnInside: !0,
                        midClick: !0,
                        callbacks: {
                            beforeOpen: function () {
                                this.st.image.markup = this.st.image.markup.replace("mfp-figure", "mfp-figure mfp-with-anim"), this.st.mainClass = "mfp-zoom-out"
                            }, open: function () {
                                e(this.content).find("video").length > 0 && e(this.content).find("video").get(0).play()
                            }, close: function () {
                                e(this.content).find("video").length > 0 && e(this.content).find("video").get(0).load()
                            }
                        }
                    }, 0)
                }, t) : void 0 === Cookies.get(s) && setTimeout(function () {
                    e.magnificPopup.open({
                        items: {src: a},
                        type: "inline",
                        closeBtnInside: !0,
                        midClick: !0,
                        callbacks: {
                            beforeOpen: function () {
                                this.st.image.markup = this.st.image.markup.replace("mfp-figure", "mfp-figure mfp-with-anim"), this.st.mainClass = "mfp-zoom-out"
                            }, open: function () {
                                e(this.content).find("video").length > 0 && e(this.content).find("video").get(0).play()
                            }, close: function () {
                                e(this.content).find("video").length > 0 && e(this.content).find("video").get(0).load(), Cookies.set(s, !0, {expires: Number(n)})
                            }
                        }
                    }, 0)
                }, t)), a.find(i).click(function () {
                    return e.magnificPopup.close(), !1
                })
            }), t.length > 0 && t.each(function () {
                var a = e(this), t = a.attr("data-delay") || 3e3, n = a.attr("data-cookie-expire") || 365,
                    r = a.attr("data-cookie-name") || "cookieName2013", l = 1 == a.data("cookie-enabled"),
                    d = a.attr("data-delay-dismiss");
                if (a.hasClass("modal-auto-open")) {
                    var c = e(this);
                    setTimeout(function () {
                        c.addClass("modal-active"), d && setTimeout(function () {
                            a.removeClass("modal-active")
                        }, d)
                    }, t)
                }
                a.find(i).click(function () {
                    return a.removeClass("modal-active"), !1
                }), a.hasClass("cookie-notify") && (setTimeout(function () {
                    1 != l ? s.addClass("modal-active") : void 0 === Cookies.get(r) && s.addClass("modal-active")
                }, t), o.click(function () {
                    return Cookies.set(r, !0, {expires: Number(n)}), e.magnificPopup.close(), s.removeClass("modal-active"), !1
                }))
            }), n.length > 0 && n.each(function () {
                var a = e(this), t = a.attr("data-modal");
                a.click(function () {
                    return e(t).toggleClass("modal-active", 1e3), !1
                })
            })
        }, notification: function (a, t, n, i, s, o, r, l, d, c) {
            var u, p;
            r = r || "fadeInDown", l = l || "fadeOutDown", o = o || "top", i ? (u = "element-container", r = "fadeIn", l = "fadeOut") : u = "col-11 col-md-4", d && (p = 'style="background-image:url(' + d + '); background-repeat: no-repeat; background-position: 50% 20%; height:120px !important; width:430px !important; border:0px;" '), t || (t = ""), i = "body";
            var f = function () {
                e.notify({title: a, message: t}, {
                    element: i,
                    type: n || "warning",
                    delay: s || 1e4,
                    template: '<div data-notify="container" ' + p + ' class="bootstrap-notify ' + u + ' alert alert-{0}" role="alert"><button type="button" aria-hidden="true" class="close" data-notify="dismiss">×</button><span data-notify="icon"></span> <span data-notify="title">{1}</span> <span data-notify="message">{2}</span></div>',
                    mouse_over: !0,
                    allow_dismiss: !0,
                    placement: {from: o},
                    animate: {enter: "animated " + r, exit: "animated " + l}
                })
            };
            c ? setTimeout(function () {
                f()
            }, 2e3) : f()
        }
    }, e(document).ready(function () {
        AFM.core.functions(), AFM.header.functions(), AFM.elements.functions()
    }), a.on("scroll", function () {
        AFM.header.stickyHeader(), AFM.core.scrollTop(), AFM.header.dotsMenu()
    }), a.on("resize", function () {
        AFM.header.logoStatus(), AFM.header.stickyHeader()
    })
}(jQuery);