
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
    document.querySelectorAll(".load-comments").forEach(button => {
      button.addEventListener("click", () => {
        const global = cfg.giscus || {};
        const settings = giscusSettingsFor(button);
        const host = button.closest("section")?.querySelector(".comments-box") ||
                     document.querySelector(`[data-comments-for="${button.dataset.mechanism}"]`);
        if (!host) return;
        host.innerHTML = "";

        if (!global.enabled || !global.repo || !global.repoId || !settings.category || !settings.categoryId) {
          host.innerHTML = '<div class="comments-placeholder">The discussion channel is ready, but its giscus repository/category settings are not configured yet.</div>';
          return;
        }

        const script = document.createElement("script");
        script.src = "https://giscus.app/client.js";
        script.async = true;
        script.crossOrigin = "anonymous";
        script.dataset.repo = global.repo;
        script.dataset.repoId = global.repoId;
        script.dataset.category = settings.category;
        script.dataset.categoryId = settings.categoryId;
        script.dataset.mapping = "specific";
        script.dataset.term = settings.term;
        script.dataset.strict = "1";
        script.dataset.reactionsEnabled = "1";
        script.dataset.emitMetadata = "0";
        script.dataset.inputPosition = "top";
        script.dataset.theme = global.theme || "light";
        script.dataset.lang = global.lang || "en";
        host.appendChild(script);
      });
    });
  }

  function setupProgressButtons() {
    const completed = new Set();
    document.querySelectorAll(".looks-fine-button").forEach(button => {
      button.addEventListener("click", () => {
        const key = button.dataset.progressKey || button.dataset.pillar;
        if (key) completed.add(key);
        button.classList.add("completed");
        const text = button.querySelector("span:last-child");
        if (text) text.textContent = "Recorded: no further feedback";
      });
    });
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
