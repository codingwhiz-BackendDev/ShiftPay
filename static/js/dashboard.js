// Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
  
  // Add hover effects to KPI cards
  const kpiCards = document.querySelectorAll('.kpi-card');
  kpiCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-4px)';
    });
    card.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0)';
    });
  });

  // Add hover effects to invoice rows
  const invoiceRows = document.querySelectorAll('.invoice-row');
  invoiceRows.forEach(row => {
    row.addEventListener('mouseenter', function() {
      this.style.transform = 'translateX(4px)';
    });
    row.addEventListener('mouseleave', function() {
      this.style.transform = 'translateX(0)';
    });
  });

  // Animate chart bars on load
  const chartBars = document.querySelectorAll('.chart-bar');
  chartBars.forEach((bar, index) => {
    bar.style.animationDelay = `${0.2 + (index * 0.1)}s`;
  });

  // Navigation active state
  const navItems = document.querySelectorAll('.dash-nav-item');
  navItems.forEach(item => {
    item.addEventListener('click', function(e) {
      navItems.forEach(nav => nav.classList.remove('active'));
      this.classList.add('active');
    });
  });

  // New Invoice button click
  const newInvoiceBtn = document.querySelector('.dash-btn-primary');
  if (newInvoiceBtn) {
    newInvoiceBtn.addEventListener('click', function() {
      alert('New Invoice form will be implemented soon!');
    });
  }

  // Logout confirmation
  const logoutBtn = document.querySelector('.user-logout');
  if (logoutBtn) {
    logoutBtn.addEventListener('click', function(e) {
      if (!confirm('Are you sure you want to logout?')) {
        e.preventDefault();
      }
    });
  }

});
