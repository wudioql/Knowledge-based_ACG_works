(function () {
  'use strict';

  var navToggle = document.querySelector('.atlas-nav-toggle');
  var nav = document.getElementById('atlas-nav');

  if (navToggle && nav) {
    function closeNav() {
      navToggle.setAttribute('aria-expanded', 'false');
      nav.classList.remove('is-open');
    }

    navToggle.addEventListener('click', function () {
      var expanded = navToggle.getAttribute('aria-expanded') === 'true';
      navToggle.setAttribute('aria-expanded', String(!expanded));
      nav.classList.toggle('is-open', !expanded);
    });

    nav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', closeNav);
    });

    document.addEventListener('click', function (event) {
      if (!nav.classList.contains('is-open')) return;
      if (nav.contains(event.target) || navToggle.contains(event.target)) return;
      closeNav();
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && nav.classList.contains('is-open')) {
        closeNav();
      }
    });
  }

  var activeFilters = {
    domain: 'all',
    medium: 'all'
  };

  var filterButtons = Array.prototype.slice.call(document.querySelectorAll('.atlas-filter'));
  var cards = Array.prototype.slice.call(document.querySelectorAll('.atlas-work-card'));
  var emptyState = document.querySelector('.atlas-filter-empty');
  var resultsCount = document.querySelector('[data-results-count]');
  var resultsTotal = document.querySelector('[data-results-total]');
  var resetButton = document.querySelector('[data-reset-filters]');

  function matchesFilter(card, group, value) {
    if (value === 'all') return true;
    var data = (card.getAttribute('data-' + group) || '').split(/\s+/);
    return data.indexOf(value) !== -1;
  }

  function syncButtons() {
    filterButtons.forEach(function (candidate) {
      var group = candidate.getAttribute('data-filter-group');
      var value = candidate.getAttribute('data-filter-value');
      var isActive = activeFilters[group] === value;
      candidate.classList.toggle('is-active', isActive);
      candidate.setAttribute('aria-pressed', String(isActive));
    });

    if (resetButton) {
      var isDefault = activeFilters.domain === 'all' && activeFilters.medium === 'all';
      resetButton.disabled = isDefault;
      resetButton.setAttribute('aria-disabled', String(isDefault));
    }
  }

  function applyFilters() {
    var visibleCount = 0;
    var totalCount = cards.length;

    cards.forEach(function (card) {
      var show = matchesFilter(card, 'domain', activeFilters.domain) && matchesFilter(card, 'medium', activeFilters.medium);
      card.hidden = !show;
      if (show) visibleCount += 1;
    });

    if (emptyState) {
      emptyState.hidden = visibleCount !== 0;
    }

    if (resultsCount) {
      resultsCount.textContent = String(visibleCount);
    }

    if (resultsTotal) {
      resultsTotal.textContent = String(totalCount);
    }

    syncButtons();
  }

  filterButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      var group = button.getAttribute('data-filter-group');
      var value = button.getAttribute('data-filter-value');
      activeFilters[group] = value;
      applyFilters();
    });
  });

  if (resetButton) {
    resetButton.addEventListener('click', function () {
      activeFilters.domain = 'all';
      activeFilters.medium = 'all';
      applyFilters();
    });
  }

  applyFilters();

  var navLinks = Array.prototype.slice.call(document.querySelectorAll('.atlas-nav a[href^="#"]'));
  var sections = navLinks
    .map(function (link) {
      var id = link.getAttribute('href').slice(1);
      var section = document.getElementById(id);
      return section ? { link: link, section: section, id: id } : null;
    })
    .filter(Boolean);

  if (sections.length) {
    function updateCurrentSection() {
      var currentId = sections[0].id;
      var threshold = window.scrollY + 180;

      sections.forEach(function (item) {
        if (item.section.offsetTop <= threshold) {
          currentId = item.id;
        }
      });

      sections.forEach(function (item) {
        var isCurrent = item.id === currentId;
        item.link.classList.toggle('is-current', isCurrent);
        if (isCurrent) {
          item.link.setAttribute('aria-current', 'location');
        } else {
          item.link.removeAttribute('aria-current');
        }
      });
    }

    window.addEventListener('scroll', updateCurrentSection, { passive: true });
    window.addEventListener('resize', updateCurrentSection);
    updateCurrentSection();
  }
})();
