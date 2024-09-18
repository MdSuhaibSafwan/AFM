"use strict";
(function() {
    const COOKIE_CONSENT_COOKIE_NAME = 'cookie_consent';
    const defaultBodyCSSOverflow = window.getComputedStyle(document.body).getPropertyValue('overflow');
    let form = document.getElementById('cc_preferences_form');

    function loadAndExecuteStyles(styleNodes) {
        const validNonce = document.getElementById('cc_script').nonce;
        let staticStyle = styleNodes.shift();
        if (staticStyle) {
            let dynamicStyle;
            if (staticStyle.tagName.toLowerCase() === 'link') {
                dynamicStyle = document.createElement("link");
                dynamicStyle.onload = function() {
                    loadAndExecuteStyles(styleNodes);
                };
                dynamicStyle.href = staticStyle.getAttribute('href');
            } else {
                dynamicStyle = document.createElement("style");
                let inlineStyle = document.createTextNode(staticStyle.innerText);
                dynamicStyle.appendChild(inlineStyle);
            }
            Array.from(staticStyle.attributes).forEach(attr => {
                if (attr.name !== 'href') {
                    dynamicStyle.setAttribute(attr.name, attr.value);
                }
            });
            if (!dynamicStyle.href && validNonce) {
                dynamicStyle.nonce = validNonce;
            }
            document.body.appendChild(dynamicStyle);
            if (!dynamicStyle.href) {
                loadAndExecuteStyles(styleNodes);
            }
        }
    }
    function loadAndExecuteScripts(scriptNodes) {
        const validNonce = document.getElementById('cc_script').nonce;
        let staticScript = scriptNodes.shift();
        if (staticScript) {
            let dynamicScript = document.createElement("script");
            if (staticScript.hasAttribute('src')) {
                dynamicScript.onload = function() {
                    loadAndExecuteScripts(scriptNodes);
                };
                dynamicScript.src = staticScript.getAttribute('src');
            } else {
                let inlineScript = document.createTextNode(staticScript.innerText);
                dynamicScript.appendChild(inlineScript);
            }
            Array.from(staticScript.attributes).forEach(attr => {
                if (attr.name !== 'src') {
                    dynamicScript.setAttribute(attr.name, attr.value);
                }
            });
            if (!dynamicScript.src && validNonce) {
                dynamicScript.nonce = validNonce;
            }
            document.body.appendChild(dynamicScript);
            if (!dynamicScript.src) {
                loadAndExecuteScripts(scriptNodes);
            }
        }
    }

    function applyConditionalHTML(url) {
        fetch(url, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',  // for the request.is_ajax() to work
            },
        }).then(response => response.text()).then(html => {
            let inMemoryDiv = document.createElement('div');
            inMemoryDiv.innerHTML = html;
            let styleNodes = [];
            inMemoryDiv.querySelectorAll('style,link[rel="stylesheet"]').forEach(node => {
                styleNodes.push(node);
                inMemoryDiv.removeChild(node);
            });
            let scriptNodes = [];
            inMemoryDiv.querySelectorAll('script').forEach(scriptNode => {
                scriptNodes.push(scriptNode);
                inMemoryDiv.removeChild(scriptNode);
            });
            document.body.insertAdjacentHTML('beforeend', inMemoryDiv.innerHTML);
            loadAndExecuteStyles(styleNodes);
            loadAndExecuteScripts(scriptNodes);
        }).catch((error) => {
            console.error('Error:', error);
        });
    }

    function initForm() {
        const buttonAcceptAll = document.getElementById('cc_accept_all');
        const buttonRejectAll = document.getElementById('cc_reject_all');

        buttonAcceptAll.addEventListener('click', e => {
            e.preventDefault();
            const checkboxes = document.querySelectorAll('.cc_section_checkbox:not([disabled])');
            checkboxes.forEach(checkbox => {
                checkbox.checked = true;
            });
        });
        buttonRejectAll.addEventListener('click', e => {
            e.preventDefault();
            const checkboxes = document.querySelectorAll('.cc_section_checkbox:not([disabled])');
            checkboxes.forEach(checkbox => {
                checkbox.checked = false;
            });
        });
        form.addEventListener(
            'submit',
            e => {
                const buttonSavePreferences = document.getElementById('cc_save_preferences');
                buttonSavePreferences.disabled = true;
                const url = form.getAttribute('action');
                if (url !== location.pathname) {
                    e.preventDefault();
                    const formData = new FormData(form);
                    fetch(url, {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'X-Requested-With': 'XMLHttpRequest',  // for the request.is_ajax() to work
                        },
                    }).then(response => response.json()).then(data => {
                        data['sections'].forEach(slug => {
                            applyConditionalHTML(url + 'conditional-html/' + slug + '/');
                        });
                        closeAndDestroyDialog();
                    }).catch((error) => {
                        console.error('Error:', error);
                    });
                }
            },
            {once: true,}
        );
    }

    function initModalDialog() {
        const buttonAcceptAllCookies = document.getElementById('cc_accept_all_cookies');
        const buttonRejectAllCookies = document.getElementById('cc_reject_all_cookies');
        const buttonManageCookies = document.getElementById('cc_manage_cookies');
        const buttonClose = document.getElementById('cc_modal_close');

        buttonAcceptAllCookies.addEventListener(
            'click',
            e => {
                e.preventDefault();
                e.target.disabled = true;
                const buttonAcceptAll = document.getElementById('cc_accept_all');
                buttonAcceptAll.click();
                const buttonSavePreferences = document.getElementById('cc_save_preferences');
                buttonSavePreferences.click();
            },
            {once: true,}
        );
        buttonRejectAllCookies.addEventListener(
            'click',
            e => {
                e.preventDefault();
                e.target.disabled = true;
                const buttonRejectAll = document.getElementById('cc_reject_all');
                buttonRejectAll.click();
                const buttonSavePreferences = document.getElementById('cc_save_preferences');
                buttonSavePreferences.click();
            },
            {once: true,}
        );
        buttonManageCookies.addEventListener(
            'click',
            e => {
                e.preventDefault();
                e.target.disabled = true;
                document.getElementById('cc_section_quick_info').classList.add('cc-hidden');
                document.getElementById('cc_section_manage_cookies').classList.remove('cc-hidden');
            },
            {once: true,}
        );
        buttonClose.addEventListener('click', e => {
            e.preventDefault();
            closeAndDestroyDialog();
        });
        buttonAcceptAllCookies.focus();
    }

    function openModalDialog() {
        const thisScript = document.getElementById('cc_script');
        const url = thisScript.getAttribute('data-modal-dialog-url');

        fetch(url, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',  // for the request.is_ajax() to work
            },
        }).then(response => response.text()).then(html => {
            const inMemoryDiv = document.createElement('div');
            inMemoryDiv.innerHTML = html;
            let scriptNodes = [];
            inMemoryDiv.querySelectorAll('script').forEach(scriptNode => {
                scriptNodes.push(scriptNode);
                inMemoryDiv.removeChild(scriptNode);
            });
            document.body.insertAdjacentHTML('beforeend', inMemoryDiv.innerHTML);
            scriptNodes.forEach(staticScript => {
                const dynamicScript = document.createElement("script");
                if (staticScript.hasAttribute('src')) {
                    dynamicScript.src = staticScript.getAttribute('src');
                } else {
                    const inlineScript = document.createTextNode(staticScript.innerText);
                    dynamicScript.appendChild(inlineScript);
                }
                Array.from(staticScript.attributes).forEach(attr => {
                    if (attr.name !== 'src') {
                        dynamicScript.setAttribute(attr.name, attr.value);
                    }
                });
                document.body.appendChild(dynamicScript);
            });
            form = document.getElementById('cc_preferences_form');
            initForm();
            initModalDialog();
            document.body.style.overflow = 'hidden';
        }).catch((error) => {
            console.error('Error:', error);
        });
    }

    function closeAndDestroyDialog() {
        document.body.style.overflow = defaultBodyCSSOverflow;
        const modalDialog = document.getElementById('cc_modal_window');
        if (modalDialog) {
            modalDialog.remove();
        }
    }

    function isCookieConsentSet() {
        const regex = new RegExp(
            '^(.*;)?\\s*' + COOKIE_CONSENT_COOKIE_NAME + '\\s*=\\s*[^;]+(.*)?$'
        );
        return document.cookie.match(regex);
    }

    if (form) {
        initForm();
    } else if (!form && !isCookieConsentSet()) {
        openModalDialog();
    }

})();
