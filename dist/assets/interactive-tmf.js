
(() => {
  "use strict";

  const cfg = window.TMF_FEEDBACK_CONFIG || {};
  const isUrl = value => typeof value === "string" && /^https?:\/\//i.test(value);

  function showNotice(origin, message) {
    const host = origin.closest("section, article, .action-card, .review-copy") || origin.parentElement;
    if (!host) return;
    let note = host.querySelector(":scope > .link-notice");
    if (!note) {
      note = document.createElement("div");
      note.className = "link-notice";
      host.appendChild(note);
    }
    note.textContent = message;
    note.classList.add("visible");
    clearTimeout(note._timer);
    note._timer = setTimeout(() => note.classList.remove("visible"), 3500);
  }

  function setupMenus() {
    document.querySelectorAll(".primary-site-menu").forEach(menu => {
      const toggles = [...menu.querySelectorAll(".menu-toggle")];
      const submenus = [...menu.querySelectorAll(".primary-submenu")];
      const timers = new Map();

      const close = (toggle, submenu, delay = 0) => {
        clearTimeout(timers.get(submenu));
        const id = setTimeout(() => {
          submenu.classList.remove("open");
          toggle.setAttribute("aria-expanded", "false");
        }, delay);
        timers.set(submenu, id);
      };

      const open = (toggle, submenu) => {
        submenus.forEach(other => {
          if (other !== submenu) {
            other.classList.remove("open");
            const otherToggle = toggles.find(t => t.dataset.menuGroup === other.dataset.menuSubgroup);
            if (otherToggle) otherToggle.setAttribute("aria-expanded", "false");
          }
        });
        clearTimeout(timers.get(submenu));
        submenu.classList.add("open");
        toggle.setAttribute("aria-expanded", "true");
      };

      toggles.forEach(toggle => {
        const submenu = menu.querySelector(`.primary-submenu[data-menu-subgroup="${toggle.dataset.menuGroup}"]`);
        if (!submenu) return;

        toggle.addEventListener("click", e => {
          e.preventDefault();
          e.stopPropagation();
          submenu.classList.contains("open") ? close(toggle, submenu) : open(toggle, submenu);
        });
        toggle.addEventListener("mouseenter", () => open(toggle, submenu));
        toggle.addEventListener("mouseleave", () => close(toggle, submenu, 850));
        submenu.addEventListener("mouseenter", () => open(toggle, submenu));
        submenu.addEventListener("mouseleave", () => close(toggle, submenu, 850));
        submenu.querySelectorAll("a").forEach(a => a.addEventListener("click", () => close(toggle, submenu)));
      });

      document.addEventListener("click", e => {
        if (!e.target.closest(".primary-site-menu")) {
          toggles.forEach(toggle => {
            const submenu = menu.querySelector(`.primary-submenu[data-menu-subgroup="${toggle.dataset.menuGroup}"]`);
            if (submenu) close(toggle, submenu);
          });
        }
      });
    });
  }

  function setupReveal() {
    const elements = document.querySelectorAll(".reveal");
    if (!("IntersectionObserver" in window)) {
      elements.forEach(el => el.classList.add("visible"));
      return;
    }
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    elements.forEach(el => observer.observe(el));
  }

  function setupSequences() {
    document.querySelectorAll(".hero-background-sequence").forEach(sequence => {
      const frames = [...sequence.querySelectorAll(".hero-bg-frame")];
      if (frames.length < 2) return;
      let index = Math.max(0, frames.findIndex(f => f.classList.contains("active")));
      setInterval(() => {
        frames[index].classList.remove("active");
        index = (index + 1) % frames.length;
        frames[index].classList.add("active");
      }, 5200);
    });

    const questionFrames = [...document.querySelectorAll(".question-visual")];
    if (questionFrames.length > 1) {
      let i = 0;
      questionFrames[0].classList.add("active");
      setInterval(() => {
        questionFrames[i].classList.remove("active");
        i = (i + 1) % questionFrames.length;
        questionFrames[i].classList.add("active");
      }, 4300);
    }
  }

  function setupZoom() {
    const levels = {};
    document.querySelectorAll("[data-zoom-target]").forEach(control => {
      control.addEventListener("click", () => {
        const id = control.dataset.zoomTarget;
        const target = document.getElementById(id);
        if (!target) return;
        levels[id] = levels[id] || 1;
        if (control.dataset.zoomAction === "in") levels[id] = Math.min(2.8, levels[id] + .15);
        if (control.dataset.zoomAction === "out") levels[id] = Math.max(.65, levels[id] - .15);
        if (control.dataset.zoomAction === "reset") levels[id] = 1;
        target.style.transform = `scale(${levels[id]})`;
      });
    });
  }

  function setupLightbox() {
    const modal = document.createElement("div");
    modal.className = "image-lightbox";
    modal.innerHTML = '<button type="button" aria-label="Close image">×</button><img alt=""><div class="lightbox-caption"></div>';
    document.body.appendChild(modal);
    const modalImage = modal.querySelector("img");
    const caption = modal.querySelector(".lightbox-caption");

    const close = () => modal.classList.remove("open");
    modal.querySelector("button").addEventListener("click", close);
    modal.addEventListener("click", e => { if (e.target === modal) close(); });
    document.addEventListener("keydown", e => { if (e.key === "Escape") close(); });

    document.querySelectorAll(".interactive-visual img, .mechanism-card-figure img").forEach(img => {
      img.closest(".interactive-visual")?.classList.add("is-clickable");
      img.addEventListener("click", e => {
        if (img.closest("a")) return;
        e.preventDefault();
        modalImage.src = img.currentSrc || img.src;
        modalImage.alt = img.alt || "";
        const title = img.closest(".visual-card")?.querySelector("h3")?.textContent || img.alt || "";
        caption.textContent = title;
        modal.classList.add("open");
      });
    });
  }

  function setupFeedbackForms() {
    document.querySelectorAll(".structured-poll-link").forEach(link => {
      const section = link.closest(".pillar-section");
      const item = section ? cfg.sections?.[section.dataset.sectionKey] : null;
      const url = item?.pollUrl;
      if (isUrl(url)) {
        link.href = url;
      } else {
        link.href = "#";
        link.addEventListener("click", e => {
          e.preventDefault();
          const title = item?.pollTitle || item?.label || "this pillar";
          showNotice(link, `Create the GitHub Poll for ${title}, then paste its discussion URL into the site feedback configuration.`);
        });
      }
    });

    document.querySelectorAll(".feedback-form-link").forEach(link => {
      let item;
      if (link.dataset.feedbackPage) {
        item = cfg.feedbackPages?.[link.dataset.feedbackPage];
      } else if (link.dataset.mechanism) {
        item = cfg.mechanisms?.[link.dataset.mechanism];
      } else {
        const section = link.closest(".pillar-section");
        if (section) item = cfg.sections?.[section.dataset.sectionKey];
      }
      const url = item?.googleFormUrl;
      if (isUrl(url)) {
        link.href = url;
      } else {
        link.href = "#";
        link.addEventListener("click", e => {
          e.preventDefault();
          showNotice(link, "The structured feedback form is not configured yet.");
        });
      }
    });

    document.querySelectorAll(".general-feedback-link").forEach(link => {
      if (isUrl(cfg.generalFeedbackUrl)) link.href = cfg.generalFeedbackUrl;
      else link.addEventListener("click", e => {
        e.preventDefault();
        showNotice(link, "The general feedback form is not configured yet.");
      });
    });
    document.querySelectorAll(".upload-link").forEach(link => {
      if (isUrl(cfg.uploadUrl)) link.href = cfg.uploadUrl;
      else link.addEventListener("click", e => {
        e.preventDefault();
        showNotice(link, "The material-upload link is not configured yet.");
      });
    });
    document.querySelectorAll("[data-config-link='github'], .github-footer-link").forEach(link => {
      if (isUrl(cfg.githubHubUrl)) link.href = cfg.githubHubUrl;
      else link.addEventListener("click", e => {
        e.preventDefault();
        showNotice(link, "The GitHub link is not configured yet.");
      });
    });
  }

  function giscusSettingsFor(button) {
    if (button.dataset.giscusTerm) {
      return {
        term: button.dataset.giscusTerm,
        category: button.dataset.giscusCategory || cfg.giscus?.category,
        categoryId: button.dataset.giscusCategoryId || cfg.giscus?.categoryId
      };
    }
    if (button.dataset.feedbackPage) {
      const item = cfg.feedbackPages?.[button.dataset.feedbackPage] || {};
      return {
        term: item.giscusTerm || button.dataset.feedbackPage,
        category: item.giscusCategory || cfg.giscus?.category,
        categoryId: item.giscusCategoryId || cfg.giscus?.categoryId
      };
    }
    if (button.dataset.mechanism) {
      const item = cfg.mechanisms?.[button.dataset.mechanism] || {};
      return {
        term: item.giscusTerm || button.dataset.mechanism,
        category: item.giscusCategory || cfg.giscus?.category,
        categoryId: item.giscusCategoryId || cfg.giscus?.categoryId
      };
    }
    const section = button.closest(".pillar-section");
    const item = section ? cfg.sections?.[section.dataset.sectionKey] || {} : {};
    return {
      term: item.giscusTerm || section?.dataset.giscusTerm || "tmf-general",
      category: item.giscusCategory || cfg.giscus?.category,
      categoryId: item.giscusCategoryId || cfg.giscus?.categoryId
    };
  }

  function setupGiscus() {
    const discussionSearchUrl = term =>
      `https://github.com/${encodeURIComponent((cfg.giscus || {}).repo || "IIT-redes/ESSMF")}/discussions?discussions_q=${encodeURIComponent(term)}`;

    const resetExistingGiscus = currentHost => {
      document.querySelectorAll(".comments-box").forEach(box => {
        if (box === currentHost) return;
        box.innerHTML = "";
      });
      document.querySelectorAll(".load-comments").forEach(b => {
        if (!b.closest("section")?.contains(currentHost)) {
          b.setAttribute("aria-expanded", "false");
          const lbl = b.querySelector("span:last-child");
          if (lbl) lbl.textContent = "Open discussion";
        }
      });
    };

    document.querySelectorAll(".load-comments").forEach(button => {
      button.addEventListener("click", () => {
        const global = cfg.giscus || {};
        const settings = giscusSettingsFor(button);
        const host = button.closest("section")?.querySelector(".comments-box") ||
                     document.querySelector(`[data-comments-for="${button.dataset.mechanism}"]`);
        if (!host) return;

        resetExistingGiscus(host);
        host.innerHTML = "";
        host.scrollIntoView({ behavior: "smooth", block: "center" });

        const configured = global.enabled && global.repo && global.repoId && settings.category && settings.categoryId
          && !String(settings.category).startsWith("PASTE_") && !String(settings.categoryId).startsWith("PASTE_");
        if (!configured) {
          host.innerHTML = '<div class="comments-placeholder"><strong>Giscus is configured in the page, but the repository/category details are incomplete.</strong></div>';
          return;
        }

        // Giscus is most reliable with one active widget per page.  We mount only the
        // discussion that the reviewer explicitly opens, using a unique term per pillar.
        const mount = document.createElement("div");
        mount.className = "giscus";
        mount.setAttribute("data-active-term", settings.term);
        host.appendChild(mount);

        const script = document.createElement("script");
        script.src = "https://giscus.app/client.js";
        script.async = true;
        script.crossOrigin = "anonymous";
        script.dataset.repo = global.repo;
        script.dataset.repoId = global.repoId;
        script.dataset.category = settings.category;
        script.dataset.categoryId = settings.categoryId;
        script.dataset.mapping = global.mapping || "specific";
        script.dataset.term = settings.term;
        script.dataset.strict = String(global.strict ?? "0");
        script.dataset.reactionsEnabled = String(global.reactionsEnabled ?? "1");
        script.dataset.emitMetadata = String(global.emitMetadata ?? "0");
        script.dataset.inputPosition = global.inputPosition || "top";
        script.dataset.theme = global.theme || "light";
        script.dataset.lang = global.lang || "en";
        if (global.loading) script.dataset.loading = global.loading;
        host.appendChild(script);

        button.setAttribute("aria-expanded", "true");
        const label = button.querySelector("span:last-child");
        if (label) label.textContent = "Discussion opened";

        // Helpful fallback: if the iframe does not appear, the most common reasons are
        // testing from file:// instead of HTTP(S), or the Giscus GitHub App not being
        // installed/authorised for this repository.
        window.setTimeout(() => {
          if (!host.querySelector(".giscus-frame")) {
            const helper = document.createElement("div");
            helper.className = "comments-placeholder giscus-diagnostic";
            helper.innerHTML = `<strong>The discussion widget has not loaded yet.</strong><br>
              Test the site through GitHub Pages or <code>preview_local.bat</code> (not by double-clicking the HTML file), and confirm that the Giscus GitHub App has access to <strong>${global.repo}</strong>.<br>
              <a href="${discussionSearchUrl(settings.term)}" target="_blank" rel="noopener">Open/search this pillar discussion directly on GitHub</a> ·
              <a href="https://github.com/apps/giscus" target="_blank" rel="noopener">Check Giscus App access</a>`;
            host.appendChild(helper);
          }
        }, 9000);
      });
    });
  }

  function setupProgressButtons() {
    const buttons = [...document.querySelectorAll(".looks-fine-button")];
    if (!buttons.length) return;

    const storageKey = "tmf-feedback-progress:" + location.pathname.replace(/[^a-z0-9_-]+/gi, "-");
    const uniqueKeys = [...new Set(buttons.map(b => b.dataset.progressKey || b.dataset.pillar).filter(Boolean))];
    const total = uniqueKeys.length || buttons.length;
    const percentEl = document.getElementById("progress-percent");
    const fillEl = document.getElementById("progress-fill");
    const progressBox = document.querySelector(".feedback-progress");
    const celebration = document.getElementById("celebration");

    const safeLoad = () => {
      try {
        const raw = localStorage.getItem(storageKey);
        return new Set((raw ? JSON.parse(raw) : []).filter(Boolean));
      } catch (_) {
        return new Set();
      }
    };
    const completed = safeLoad();
    const safeSave = () => {
      try { localStorage.setItem(storageKey, JSON.stringify([...completed])); } catch (_) { /* local file preview may block storage */ }
    };

    const launchLightCelebration = () => {
      document.querySelectorAll('.tmf-light-show,.tmf-party-show').forEach(el => el.remove());

      const light = document.createElement('div');
      light.className = 'tmf-light-show';
      light.setAttribute('aria-hidden','true');
      for (let i=0; i<34; i++) {
        const spark = document.createElement('span');
        spark.className = 'tmf-spark';
        spark.style.setProperty('--x', (Math.random()*100).toFixed(2) + 'vw');
        spark.style.setProperty('--y', (Math.random()*100).toFixed(2) + 'vh');
        spark.style.setProperty('--delay', (Math.random()*1.1).toFixed(2) + 's');
        spark.style.setProperty('--scale', (0.55 + Math.random()*1.65).toFixed(2));
        light.appendChild(spark);
      }
      document.body.appendChild(light);

      const party = document.createElement('div');
      party.className = 'tmf-party-show';
      party.setAttribute('aria-hidden','true');
      const confettiShapes = ['■','●','◆','▲','▰'];
      for (let i=0; i<90; i++) {
        const c = document.createElement('span');
        c.className = 'tmf-confetti';
        c.textContent = confettiShapes[Math.floor(Math.random()*confettiShapes.length)];
        c.style.setProperty('--x', (Math.random()*100).toFixed(2) + 'vw');
        c.style.setProperty('--delay', (Math.random()*1.3).toFixed(2) + 's');
        c.style.setProperty('--dur', (2.8 + Math.random()*2.3).toFixed(2) + 's');
        c.style.setProperty('--rot', (360 + Math.random()*1080).toFixed(0) + 'deg');
        c.style.setProperty('--hue', (Math.random()*360).toFixed(0));
        party.appendChild(c);
      }
      for (let i=0; i<22; i++) {
        const ch = document.createElement('span');
        ch.className = 'tmf-chocolate';
        ch.textContent = ['🍫','🍬','🍪'][i%3];
        ch.style.setProperty('--x', (3 + Math.random()*94).toFixed(2) + 'vw');
        ch.style.setProperty('--delay', (Math.random()*1.15).toFixed(2) + 's');
        ch.style.setProperty('--dur', (3.0 + Math.random()*1.7).toFixed(2) + 's');
        ch.style.setProperty('--s', (0.8 + Math.random()*1.0).toFixed(2));
        party.appendChild(ch);
      }
      document.body.appendChild(party);
      document.body.classList.add('tmf-review-complete');
      setTimeout(() => document.body.classList.remove('tmf-review-complete'), 5200);
      setTimeout(() => light.remove(), 6100);
      setTimeout(() => party.remove(), 6500);
    };

    const update = (flash=false) => {
      buttons.forEach(button => {
        const key = button.dataset.progressKey || button.dataset.pillar;
        const done = key && completed.has(key);
        button.classList.toggle("completed", !!done);
        button.setAttribute('aria-pressed', done ? 'true' : 'false');
        const text = button.querySelector("span:last-child");
        if (text) text.textContent = done ? "Recorded: no further feedback" : "No further feedback";
      });
      const count = uniqueKeys.filter(k => completed.has(k)).length;
      const pct = total ? Math.round((count / total) * 100) : 0;
      if (percentEl) percentEl.textContent = pct + "%";
      if (fillEl) fillEl.style.width = pct + "%";
      if (progressBox) {
        progressBox.setAttribute('aria-valuemin','0');
        progressBox.setAttribute('aria-valuemax','100');
        progressBox.setAttribute('aria-valuenow',String(pct));
        progressBox.classList.toggle('complete', pct >= 100);
      }
      safeSave();
      if (pct >= 100 && celebration && flash) {
        celebration.innerHTML = "<strong>100% — review completed!</strong><span>Thank you sincerely for your time, expertise, and contribution. Your feedback helps us build a clearer common language for European flexibility-market design.</span><i>🎉 🍫 🎊</i>";
        celebration.classList.add("show", "pulse-once");
        launchLightCelebration();
        setTimeout(() => celebration.classList.remove("show", "pulse-once"), 5200);
      }
    };

    buttons.forEach(button => {
      button.addEventListener("click", () => {
        const key = button.dataset.progressKey || button.dataset.pillar;
        if (!key) return;
        const wasComplete = uniqueKeys.every(k => completed.has(k));
        completed.add(key);
        const nowComplete = uniqueKeys.every(k => completed.has(k));
        update(nowComplete && !wasComplete);
      });
    });
    update(false);
  }

  function setupActiveNavigation() {
    const anchors = [...document.querySelectorAll(".primary-submenu a[href^='#']")];
    if (!anchors.length) return;
    const items = anchors.map(a => ({ a, el: document.querySelector(a.getAttribute("href")) })).filter(x => x.el);
    const update = () => {
      const marker = scrollY + Math.max(110, innerHeight * .3);
      let current = items[0];
      items.forEach(item => { if (item.el.offsetTop <= marker) current = item; });
      anchors.forEach(a => a.classList.toggle("active", current && a === current.a));
      document.querySelectorAll(".menu-toggle").forEach(toggle => {
        const submenu = toggle.nextElementSibling;
        toggle.classList.toggle("active", !!submenu?.querySelector("a.active"));
      });
    };
    addEventListener("scroll", update, { passive: true });
    addEventListener("resize", update);
    update();
  }

  document.addEventListener("DOMContentLoaded", () => {
    setupMenus();
    setupReveal();
    setupSequences();
    setupZoom();
    setupLightbox();
    setupFeedbackForms();
    setupGiscus();
    setupProgressButtons();
    setupActiveNavigation();
  });
})();
