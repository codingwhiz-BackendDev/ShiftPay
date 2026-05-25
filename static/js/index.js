// ─── SCROLL REVEAL ───
const reveals = document.querySelectorAll(".reveal");
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) {
        e.target.classList.add("visible");
        observer.unobserve(e.target);
      }
    });
  },
  { threshold: 0.1, rootMargin: "0px 0px -40px 0px" },
);
reveals.forEach((el) => observer.observe(el));

// ─── NAVBAR SCROLL EFFECT ───
const nav = document.querySelector("nav");
window.addEventListener("scroll", () => {
  nav.style.background =
    window.scrollY > 60 ? "rgba(8,12,24,0.92)" : "rgba(8,12,24,0.7)";
});

// ─── ANIMATED COUNTERS ───
const counters = [
  {
    el: null,
    target: 4200000000,
    prefix: "₦",
    suffix: "B+",
    divisor: 1000000000,
    decimals: 1,
  },
  { el: null, target: 12400, prefix: "", suffix: "+", divisor: 1, decimals: 0 },
  { el: null, target: 94, prefix: "", suffix: "%", divisor: 1, decimals: 0 },
];
const metricNums = document.querySelectorAll(".metric-num");
let countersStarted = false;

function animateCounter(el, target, prefix, suffix, divisor, decimals) {
  const duration = 2000;
  const start = performance.now();
  const step = (now) => {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    const value = (target * eased) / divisor;
    el.textContent = prefix + value.toFixed(decimals) + suffix;
    if (progress < 1) requestAnimationFrame(step);
  };
  requestAnimationFrame(step);
}

const metricsStrip = document.querySelector(".metrics-strip");
const stripObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting && !countersStarted) {
        countersStarted = true;
        animateCounter(metricNums[0], 4.2, "₦", "B+", 1, 1);
        animateCounter(metricNums[1], 12400, "", "+", 1, 0);
        animateCounter(metricNums[2], 94, "", "%", 1, 0);
      }
    });
  },
  { threshold: 0.3 },
);
if (metricsStrip) stripObserver.observe(metricsStrip);

// ─── SMOOTH MOUSE PARALLAX ON HERO VISUAL ───
const heroVisual = document.querySelector(".hero-visual");
if (heroVisual) {
  document.addEventListener("mousemove", (e) => {
    const x = (e.clientX / window.innerWidth - 0.5) * 12;
    const y = (e.clientY / window.innerHeight - 0.5) * 8;
    heroVisual.style.transform = `translate(${x * 0.3}px, ${y * 0.3}px)`;
  });
}

// ─── HERO ENTRANCE STAGGER ───
const heroContent = document.querySelector(".hero-content");
if (heroContent) {
  const children = heroContent.children;
  Array.from(children).forEach((child, i) => {
    child.style.opacity = "0";
    child.style.transform = "translateY(24px)";
    child.style.transition = `opacity 0.7s ease ${i * 0.12}s, transform 0.7s ease ${i * 0.12}s`;
    setTimeout(
      () => {
        child.style.opacity = "1";
        child.style.transform = "translateY(0)";
      },
      100 + i * 120,
    );
  });
}

// ─── DASHBOARD MOCKUP ENTRANCE ───
const mockup = document.querySelector(".dashboard-mockup");
if (mockup) {
  mockup.style.opacity = "0";
  mockup.style.transform = "translateY(40px) scale(0.97)";
  mockup.style.transition = "opacity 0.9s ease 0.5s, transform 0.9s ease 0.5s";
  setTimeout(() => {
    mockup.style.opacity = "1";
    mockup.style.transform = "translateY(0) scale(1)";
  }, 200);
}
