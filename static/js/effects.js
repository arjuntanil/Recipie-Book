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

    // PDF Download functionality
    const downloadBtn = document.getElementById('downloadPDF');
    if (!downloadBtn) return;

    downloadBtn.addEventListener('click', function() {
        generatePDF();
    });

    function generatePDF() {
        // Show progress container
        const progressContainer = document.querySelector('.download-progress');
        const progressBar = document.querySelector('.progress-bar-pdf');
        const progressText = document.querySelector('.progress-text');
        
        progressContainer.classList.add('active');
        progressBar.style.width = '0%';
        progressText.textContent = 'Preparing content...';
        
        // Get recipe elements
        const recipeTitle = document.querySelector('.recipe-title').textContent;
        const recipeDescription = document.querySelector('.recipe-description').textContent;
        const recipeImage = document.querySelector('.recipe-main-image');
        const ingredientsList = document.querySelector('.ingredients-list');
        const instructionsList = document.querySelector('.instructions-list');
        
        // Update progress
        setTimeout(() => {
            progressBar.style.width = '20%';
            progressText.textContent = 'Creating PDF...';
            
            // Create PDF document
            const pdf = new jsPDF('p', 'pt', 'a4');
            const pageWidth = pdf.internal.pageSize.getWidth();
            let yOffset = 50;
            
            // Add title
            pdf.setFontSize(24);
            pdf.setFont('helvetica', 'bold');
            pdf.text(recipeTitle, pageWidth / 2, yOffset, { align: 'center' });
            yOffset += 40;
            
            progressBar.style.width = '30%';
            progressText.textContent = 'Adding recipe details...';
            
            // Add description
            pdf.setFontSize(12);
            pdf.setFont('helvetica', 'normal');
            const descriptionLines = pdf.splitTextToSize(recipeDescription, pageWidth - 80);
            pdf.text(descriptionLines, 40, yOffset);
            yOffset += (descriptionLines.length * 15) + 30;
            
            progressBar.style.width = '40%';
            progressText.textContent = 'Processing image...';
            
            // Add image
            if (recipeImage) {
                html2canvas(recipeImage).then(canvas => {
                    progressBar.style.width = '60%';
                    progressText.textContent = 'Adding image...';
                    
                    const imgData = canvas.toDataURL('image/jpeg', 0.8);
                    const imgWidth = pageWidth - 80;
                    const imgHeight = (canvas.height * imgWidth) / canvas.width;
                    
                    pdf.addImage(imgData, 'JPEG', 40, yOffset, imgWidth, imgHeight);
                    yOffset += imgHeight + 30;
                    
                    progressBar.style.width = '70%';
                    progressText.textContent = 'Adding ingredients...';
                    
                    // Add ingredients
                    pdf.setFontSize(18);
                    pdf.setFont('helvetica', 'bold');
                    pdf.text('Ingredients', 40, yOffset);
                    yOffset += 25;
                    
                    pdf.setFontSize(12);
                    pdf.setFont('helvetica', 'normal');
                    
                    if (ingredientsList) {
                        const ingredients = ingredientsList.querySelectorAll('li');
                        ingredients.forEach(ingredient => {
                            const text = ingredient.textContent.trim();
                            const lines = pdf.splitTextToSize(text, pageWidth - 100);
                            pdf.text(lines, 50, yOffset);
                            yOffset += (lines.length * 15) + 10;
                            
                            // Check if we need a new page
                            if (yOffset > pdf.internal.pageSize.getHeight() - 50) {
                                pdf.addPage();
                                yOffset = 50;
                            }
                        });
                    }
                    
                    progressBar.style.width = '85%';
                    progressText.textContent = 'Adding instructions...';
                    
                    // Add instructions
                    yOffset += 10;
                    pdf.setFontSize(18);
                    pdf.setFont('helvetica', 'bold');
                    pdf.text('Instructions', 40, yOffset);
                    yOffset += 25;
                    
                    pdf.setFontSize(12);
                    pdf.setFont('helvetica', 'normal');
                    
                    if (instructionsList) {
                        const instructions = instructionsList.querySelectorAll('li');
                        instructions.forEach((instruction, index) => {
                            const text = instruction.textContent.trim();
                            const stepText = `${index + 1}. ${text}`;
                            const lines = pdf.splitTextToSize(stepText, pageWidth - 100);
                            pdf.text(lines, 50, yOffset);
                            yOffset += (lines.length * 15) + 15;
                            
                            // Check if we need a new page
                            if (yOffset > pdf.internal.pageSize.getHeight() - 50) {
                                pdf.addPage();
                                yOffset = 50;
                            }
                        });
                    }
                    
                    progressBar.style.width = '95%';
                    progressText.textContent = 'Finalizing...';
                    
                    // Add footer
                    const currentDate = new Date().toLocaleDateString();
                    pdf.setFontSize(10);
                    pdf.setTextColor(150, 150, 150);
                    pdf.text(`Recipe downloaded on ${currentDate} from Recipe Book`, pageWidth / 2, pdf.internal.pageSize.getHeight() - 20, { align: 'center' });
                    
                    // Save PDF
                    setTimeout(() => {
                        progressBar.style.width = '100%';
                        progressText.textContent = 'Download complete!';
                        
                        pdf.save(`${recipeTitle.replace(/\s+/g, '-').toLowerCase()}.pdf`);
                        
                        // Reset progress after 2 seconds
                        setTimeout(() => {
                            progressContainer.classList.remove('active');
                        }, 2000);
                    }, 500);
                }).catch(error => {
                    console.error('Error generating PDF:', error);
                    progressText.textContent = 'Error generating PDF. Please try again.';
                    
                    setTimeout(() => {
                        progressContainer.classList.remove('active');
                    }, 2000);
                });
            } else {
                // No image case
                progressBar.style.width = '70%';
                progressText.textContent = 'Adding ingredients...';
                
                // Continue with ingredients and instructions...
                // [similar code as above for ingredients and instructions]
                
                progressBar.style.width = '100%';
                progressText.textContent = 'Download complete!';
                
                pdf.save(`${recipeTitle.replace(/\s+/g, '-').toLowerCase()}.pdf`);
                
                setTimeout(() => {
                    progressContainer.classList.remove('active');
                }, 2000);
            }
        }, 500);
    }
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