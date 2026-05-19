// ============================================
// 行业信源站 - 前端交互脚本
// ============================================

document.addEventListener('DOMContentLoaded', function() {
    // 移动端菜单切换
    const navToggle = document.querySelector('.nav-toggle');
    const navList = document.querySelector('.nav-list');
    
    if (navToggle && navList) {
        navToggle.addEventListener('click', function() {
            navList.classList.toggle('active');
        });
    }
    
    // 移动端下拉菜单点击展开
    const hasDropdowns = document.querySelectorAll('.has-dropdown');
    
    if (hasDropdowns.length > 0) {
        hasDropdowns.forEach(function(item) {
            const link = item.querySelector('.nav-link');
            
            if (link) {
                link.addEventListener('click', function(e) {
                    // 移动端点击展开下拉菜单
                    if (window.innerWidth <= 768) {
                        e.preventDefault();
                        item.classList.toggle('active');
                    }
                });
            }
        });
        
        // 点击菜单外关闭下拉
        document.addEventListener('click', function(e) {
            if (window.innerWidth <= 768) {
                if (!e.target.closest('.has-dropdown')) {
                    hasDropdowns.forEach(function(item) {
                        item.classList.remove('active');
                    });
                }
            }
        });
    }
    
    // 平滑滚动
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    // 图片懒加载
    if ('loading' in HTMLImageElement.prototype) {
        // 浏览器原生支持
        document.querySelectorAll('img[loading="lazy"]').forEach(img => {
            img.src = img.dataset.src || img.src;
        });
    } else {
        // 降级处理：使用 Intersection Observer
        const lazyImages = document.querySelectorAll('img[loading="lazy"]');
        
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src || img.src;
                        imageObserver.unobserve(img);
                    }
                });
            });
            
            lazyImages.forEach(img => imageObserver.observe(img));
        }
    }
    
    // 搜索框交互
    const searchInput = document.querySelector('.search-form input');
    const searchForm = document.querySelector('.search-form');
    
    if (searchInput && searchForm) {
        searchInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !this.value.trim()) {
                e.preventDefault();
                this.focus();
            }
        });
    }
    
    // 复制代码高亮（可选）
    document.querySelectorAll('pre code').forEach(block => {
        block.parentElement.setAttribute('tabindex', '0');
    });
    
    // 返回顶部
    const scrollTop = document.createElement('button');
    scrollTop.className = 'scroll-top';
    scrollTop.innerHTML = '↑';
    scrollTop.setAttribute('aria-label', '返回顶部');
    document.body.appendChild(scrollTop);
    
    scrollTop.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: var(--primary-color, #0066CC);
        color: white;
        border: none;
        cursor: pointer;
        font-size: 1.25rem;
        opacity: 0;
        transition: opacity 0.3s;
        z-index: 99;
    `;
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            scrollTop.style.opacity = '1';
        } else {
            scrollTop.style.opacity = '0';
        }
    });
    
    scrollTop.addEventListener('click', function() {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
});
