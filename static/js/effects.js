/**
 * Recipe Book Premium Animations and Effects
 * This file contains all custom animations and interactive effects
 */

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Check if we're on the recipe detail page
    if (document.querySelector('.recipe-detail-page')) {
        initRecipeDetailEffects();
    }
    
    // Initialize universal effects
    initUniversalEffects();
});

/**
 * Initialize effects specific to the recipe detail page
 */
function initRecipeDetailEffects() {
    // Enhanced 3D Parallax effect for recipe hero
    const parallaxContainer = document.querySelector('.parallax-container');
    const parallaxBg = document.querySelector('.parallax-bg');
    
    if (parallaxContainer && parallaxBg) {
        // Scroll parallax
        window.addEventListener('scroll', function() {
            const scrollPosition = window.pageYOffset;
            const translateY = scrollPosition * 0.3;
            const scale = 1 + (scrollPosition * 0.0003);
            
            parallaxBg.style.transform = `translateY(${translateY}px) scale(${scale})`;
        });
        
        // Mouse movement parallax
        document.addEventListener('mousemove', function(e) {
            if (window.innerWidth < 768) return; // Disable on mobile
            
            const mouseX = e.clientX / window.innerWidth - 0.5;
            const mouseY = e.clientY / window.innerHeight - 0.5;
            
            // Subtle mouse parallax
            parallaxBg.style.transform = `translate(${mouseX * 20}px, ${mouseY * 20}px) scale(1.1)`;
        });
    }
    
    // Floating stats panel behavior
    const statsPanel = document.querySelector('.stats-panel');
    
    if (statsPanel) {
        const initialOffset = statsPanel.offsetTop;
        const contentContainer = document.querySelector('.content-container');
        
        window.addEventListener('scroll', function() {
            const scrollPosition = window.pageYOffset;
            const contentBottom = contentContainer.offsetTop + contentContainer.offsetHeight;
            
            // Make stats panel float when scrolling
            if (scrollPosition > initialOffset - 20 && scrollPosition < contentBottom - statsPanel.offsetHeight - 100) {
                statsPanel.classList.add('floating');
                statsPanel.style.transform = `translateY(${scrollPosition - initialOffset + 120}px)`;
            } else if (scrollPosition <= initialOffset - 20) {
                statsPanel.classList.remove('floating');
                statsPanel.style.transform = 'translateY(0)';
            } else if (scrollPosition >= contentBottom - statsPanel.offsetHeight - 100) {
                statsPanel.style.transform = `translateY(${contentBottom - statsPanel.offsetHeight - initialOffset - 100}px)`;
            }
        });
    }
    
    // Interactive ingredients list
    const ingredientItems = document.querySelectorAll('.ingredient-item');
    
    ingredientItems.forEach(item => {
        item.addEventListener('click', function() {
            const checkbox = this.querySelector('.ingredient-checkbox');
            const textElement = this.querySelector('.ingredient-text');
            
            checkbox.classList.toggle('checked');
            
            if (checkbox.classList.contains('checked')) {
                textElement.style.textDecoration = 'line-through';
                textElement.style.opacity = '0.6';
            } else {
                textElement.style.textDecoration = 'none';
                textElement.style.opacity = '1';
            }
            
            // Save state to localStorage
            saveIngredientState();
        });
    });
    
    // Restore ingredient states from localStorage
    restoreIngredientState();
    
    // Intersection Observer for scroll animations
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                
                // For staggered animations on lists
                if (entry.target.classList.contains('ingredients-list') || 
                    entry.target.classList.contains('instructions-list')) {
                    
                    const items = entry.target.querySelectorAll('[data-scroll-item]');
                    items.forEach((item, index) => {
                        setTimeout(() => {
                            item.classList.add('revealed');
                        }, index * 100);
                    });
                }
                
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.15,
        rootMargin: '0px 0px -10% 0px'
    });
    
    // Observe all elements with scroll animation
    document.querySelectorAll('[data-scroll]').forEach(el => {
        observer.observe(el);
    });
    
    // Animate nutrition bars when visible
    const nutritionObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const bar = entry.target;
                const targetWidth = bar.style.width;
                
                // Reset and animate
                bar.style.width = '0%';
                setTimeout(() => {
                    bar.style.width = targetWidth;
                }, 10);
                
                nutritionObserver.unobserve(bar);
            }
        });
    }, {
        threshold: 0.1
    });
    
    document.querySelectorAll('[data-nutrition-animate]').forEach(bar => {
        nutritionObserver.observe(bar);
    });
    
    // Print functionality
    document.querySelector('.print-button')?.addEventListener('click', function(e) {
        e.preventDefault();
        window.print();
    });
}

/**
 * Initialize effects that apply to all pages
 */
function initUniversalEffects() {
    // Fade in effect for page load
    document.body.classList.add('loaded');
    
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

/**
 * Save checked ingredient states to localStorage
 */
function saveIngredientState() {
    const recipe = document.querySelector('.recipe-hero h1.title-xl')?.textContent;
    if (!recipe) return;
    
    const ingredients = document.querySelectorAll('.ingredient-item');
    const checkedState = {};
    
    ingredients.forEach((item, index) => {
        const isChecked = item.querySelector('.ingredient-checkbox')?.classList.contains('checked');
        checkedState[index] = isChecked;
    });
    
    localStorage.setItem(`recipe_${recipe.trim()}`, JSON.stringify(checkedState));
}

/**
 * Restore checked ingredient states from localStorage
 */
function restoreIngredientState() {
    const recipe = document.querySelector('.recipe-hero h1.title-xl')?.textContent;
    if (!recipe) return;
    
    const savedState = localStorage.getItem(`recipe_${recipe.trim()}`);
    if (!savedState) return;
    
    try {
        const checkedState = JSON.parse(savedState);
        const ingredients = document.querySelectorAll('.ingredient-item');
        
        ingredients.forEach((item, index) => {
            const checkbox = item.querySelector('.ingredient-checkbox');
            const textElement = item.querySelector('.ingredient-text');
            
            if (checkedState[index]) {
                checkbox.classList.add('checked');
                textElement.style.textDecoration = 'line-through';
                textElement.style.opacity = '0.6';
            }
        });
    } catch (e) {
        console.error('Error restoring ingredient state:', e);
    }
} 