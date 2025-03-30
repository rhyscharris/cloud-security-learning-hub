// Main JavaScript file for Cloud Security Learning Hub

document.addEventListener('DOMContentLoaded', function() {
    // Enable Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Close alert messages after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Form validation for quiz submission
    const quizForm = document.querySelector('form[action*="/quiz/"][action*="/submit"]'); // select form element that matches 'quiz/{id}/submit' structure
    if (quizForm) {
        quizForm.addEventListener('submit', function(event) {
            const questions = document.querySelectorAll('.card-body');
            let allAnswered = true;
            
            questions.forEach(function(question) {
                const radios = question.querySelectorAll('input[type="radio"]');
                if (radios.length > 0) {
                    let questionAnswered = false;
                    radios.forEach(function(radio) {
                        if (radio.checked) {
                            questionAnswered = true;
                        }
                    });
                    
                    if (!questionAnswered) {
                        allAnswered = false;
                        question.classList.add('border', 'border-danger'); // add red border to unanswered questions
                    } else {
                        question.classList.remove('border', 'border-danger'); // remove it if questions are now answered (but others aren't)
                    }
                }
            });
            
            if (!allAnswered) {
                event.preventDefault();
                
                // New Alert Code...
                const existingAlert = document.querySelector('.alert'); // Check if there's already an alert visible and remove it
                if (existingAlert) {
                    existingAlert.remove();
                }
                
                // Create the alert using Bootstrap classes that match the template
                const alertDiv = document.createElement('div');
                alertDiv.className = 'alert alert-warning alert-dismissible fade show';
                alertDiv.innerHTML = `
                    Please answer all questions before submitting.
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                `;
                
                // Get the container where the content block is
                const container = document.querySelector('.container.mt-4');
                
                // Insert at the beginning of the container, before the content block
                const contentBlock = document.querySelector('#content') || container.firstChild;
                container.insertBefore(alertDiv, contentBlock);
                
                window.scrollTo(0, 0); // scroll to top of page for the user
            }
        });
    }
});
