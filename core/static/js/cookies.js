/*  <!-- ========== JAVASCRIPT FOR COOKIE CONSENT ========== --> */

    (function() {
      'use strict';

      // --- Check if consent has already been given ---
      function getCookie(name) {
        const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
        if (match) return match[2];
        return null;
      }

      const banner = document.getElementById('cookieBanner');
      const consentCookie = getCookie('cookie_consent');

      // If consent already given, hide the banner
      if (consentCookie !== 'accepted') {
        banner.classList.remove('hidden');
      }

      // --- Expose accept function globally ---
      window.acceptCookies = function() {
        // Set a persistent cookie to remember the user's choice
        const expiryDate = new Date();
        expiryDate.setFullYear(expiryDate.getFullYear() + 1); // 1 year from now
        document.cookie = 'cookie_consent=accepted; path=/; expires=' + expiryDate.toUTCString() + '; Secure; SameSite=Lax';

        // Hide the banner with a smooth transition
        banner.classList.add('hidden');

        // (Optional) You could also fire a custom event here to load any deferred scripts
        // but since we only use functional cookies, there's nothing else to load.
        console.log('Cookie consent accepted. Only functional cookies are used.');
      };

      // --- Keyboard accessibility: allow Enter/Space on the button ---
      const acceptBtn = document.querySelector('.cookie-banner .btn-accept');
      if (acceptBtn) {
        acceptBtn.addEventListener('keydown', function(e) {
          if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            window.acceptCookies();
          }
        });
      }

    })();