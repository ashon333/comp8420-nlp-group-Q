// Shared Navbar component injection
document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('navbar-container');
  if (!container) return;

  const nickname = getNickname();
  const currentPath = window.location.pathname.split('/').pop() || 'index.html';

  const navItems = [
    { name: 'Home', path: 'index.html', icon: 'home' },
    { name: 'About', path: 'about.html', icon: 'info' }
  ];

  // Render navigation links
  const linksHtml = navItems.map(item => {
    // Basic match check (handles default/empty path mapping to index.html)
    const isActive = currentPath === item.path || (currentPath === '' && item.path === 'index.html');
    return `
      <a href="${item.path}" class="flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold transition-all duration-200 ${
        isActive
          ? 'bg-orange-500 text-white shadow-lg shadow-orange-500/20'
          : 'text-slate-600 hover:text-orange-500 hover:bg-orange-50/50'
      }">
        <i data-lucide="${item.icon}" class="w-4 h-4"></i>
        <span>${item.name}</span>
      </a>
    `;
  }).join('');

  // Mobile menu items
  const mobileLinksHtml = navItems.map(item => {
    const isActive = currentPath === item.path || (currentPath === '' && item.path === 'index.html');
    return `
      <a href="${item.path}" class="flex items-center gap-3 px-4 py-3 rounded-xl text-base font-semibold transition-all duration-200 ${
        isActive
          ? 'bg-orange-500 text-white shadow-md'
          : 'text-slate-600 hover:text-orange-500 hover:bg-orange-50'
      }">
        <i data-lucide="${item.icon}" class="w-5 h-5"></i>
        <span>${item.name}</span>
      </a>
    `;
  }).join('');

  const navbarHtml = `
    <nav class="bg-white/80 backdrop-blur-md sticky top-0 z-50 border-b border-slate-100">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-20 items-center">
          <!-- Logo -->
          <div class="flex items-center gap-2 cursor-pointer" onclick="window.location.href='index.html'">
            <div class="bg-orange-500 p-2 rounded-xl text-white shadow-md shadow-orange-500/10">
              <i data-lucide="shopping-cart" class="w-5 h-5"></i>
            </div>
            <span class="text-xl font-extrabold text-slate-800 tracking-tight">Congo Shop</span>
          </div>

          <!-- Nav Items (Desktop) -->
          <div class="hidden md:flex items-center space-x-4">
            ${linksHtml}
          </div>

          <!-- User Info & Actions -->
          <div class="flex items-center space-x-4">
            <span class="text-slate-500 font-semibold text-xs bg-slate-100 px-3 py-1.5 rounded-full hidden sm:block">
              Hi, ${nickname || 'Guest'}
            </span>
            <button id="signout-btn" class="bg-orange-100 hover:bg-orange-200 text-orange-600 px-4 py-2 rounded-xl font-bold transition-all text-xs flex items-center gap-2 active:scale-95">
              Sign Out <i data-lucide="log-out" class="w-3.5 h-3.5"></i>
            </button>
            <button id="mobile-menu-toggle" class="md:hidden text-slate-600 p-2 hover:bg-slate-50 rounded-xl">
              <i data-lucide="menu" class="w-6 h-6"></i>
            </button>
          </div>
        </div>
      </div>
      
      <!-- Mobile Menu (Hidden by default) -->
      <div id="mobile-menu" class="hidden md:hidden border-t border-slate-100 bg-white/95 backdrop-blur-md px-4 py-4 space-y-2 absolute top-20 left-0 right-0 shadow-lg z-40 transition-all duration-300">
        ${mobileLinksHtml}
        <div class="pt-4 border-t border-slate-100 sm:hidden">
          <span class="block px-4 py-2 text-sm font-semibold text-slate-400">Hi, ${nickname || 'Guest'}</span>
        </div>
      </div>
    </nav>
  `;

  container.innerHTML = navbarHtml;

  // Sign out listener
  const signOutBtn = document.getElementById('signout-btn');
  if (signOutBtn) {
    signOutBtn.addEventListener('click', () => {
      logoutUser();
    });
  }

  // Mobile menu toggle
  const menuToggle = document.getElementById('mobile-menu-toggle');
  const mobileMenu = document.getElementById('mobile-menu');
  if (menuToggle && mobileMenu) {
    menuToggle.addEventListener('click', () => {
      mobileMenu.classList.toggle('hidden');
    });
  }

  // Initialize Lucide icons inside the injected navbar
  if (window.lucide) {
    window.lucide.createIcons();
  }
});
