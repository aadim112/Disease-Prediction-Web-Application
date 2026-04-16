/**
 * Heart Disease Predictor — Frontend Logic
 * Handles form submission, API communication, and result display.
 */

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const btn = document.getElementById('predict-btn');
    const resultSection = document.getElementById('result-section');
    const errorToast = document.getElementById('error-toast');

    // Handle form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Validate all fields
        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }

        // Show loading state
        btn.classList.add('loading');
        btn.disabled = true;
        resultSection.classList.remove('show');

        try {
            // Collect form data
            const formData = {
                age: parseInt(document.getElementById('age').value),
                sex: parseInt(document.getElementById('sex').value),
                cp: parseInt(document.getElementById('cp').value),
                trestbps: parseInt(document.getElementById('trestbps').value),
                chol: parseInt(document.getElementById('chol').value),
                fbs: parseInt(document.getElementById('fbs').value),
                restecg: parseInt(document.getElementById('restecg').value),
                thalach: parseInt(document.getElementById('thalach').value),
                exang: parseInt(document.getElementById('exang').value),
                oldpeak: parseFloat(document.getElementById('oldpeak').value),
                slope: parseInt(document.getElementById('slope').value),
                ca: parseInt(document.getElementById('ca').value),
                thal: parseInt(document.getElementById('thal').value)
            };

            // Send prediction request
            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.error || 'Prediction failed');
            }

            const result = await response.json();
            displayResult(result);

        } catch (error) {
            showError(error.message || 'Something went wrong. Please try again.');
        } finally {
            btn.classList.remove('loading');
            btn.disabled = false;
        }
    });

    /**
     * Display prediction result with animated gauge
     */
    function displayResult(result) {
        const resultCard = document.getElementById('result-card');
        const gaugePercent = document.getElementById('gauge-percentage');
        const gaugeFill = document.getElementById('gauge-fill');
        const resultTitle = document.getElementById('result-title');
        const resultDesc = document.getElementById('result-description');
        const resultBadge = document.getElementById('result-badge');

        const isHighRisk = result.prediction === 1;
        const probability = result.probability;

        // Update card styling
        resultCard.className = `result-card ${isHighRisk ? 'high-risk' : 'low-risk'}`;

        // Update text
        resultTitle.textContent = isHighRisk ? 'Heart Disease Detected' : 'No Heart Disease Detected';
        resultDesc.textContent = isHighRisk
            ? `The model predicts a ${probability}% probability of heart disease. Please consult a healthcare professional for proper diagnosis and guidance.`
            : `The model predicts a ${(100 - probability).toFixed(1)}% probability of no heart disease. Continue maintaining a healthy lifestyle.`;
        resultBadge.textContent = isHighRisk
            ? `⚠️ High Risk — ${probability}%`
            : `✅ Low Risk — ${(100 - probability).toFixed(1)}%`;

        // Animate gauge
        const circumference = 2 * Math.PI * 70; // radius = 70
        const displayPercent = isHighRisk ? probability : (100 - probability);
        const offset = circumference - (displayPercent / 100) * circumference;

        // Reset animation
        gaugeFill.style.transition = 'none';
        gaugeFill.style.strokeDashoffset = circumference;

        // Show section
        resultSection.classList.add('show');

        // Trigger gauge animation after a brief delay
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                gaugeFill.style.transition = 'stroke-dashoffset 1.5s cubic-bezier(0.4, 0, 0.2, 1)';
                gaugeFill.style.strokeDashoffset = offset;
            });
        });

        // Animate counter
        animateCounter(gaugePercent, 0, displayPercent, 1200);

        // Scroll to result
        setTimeout(() => {
            resultSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 200);
    }

    /**
     * Animate a number counter
     */
    function animateCounter(element, start, end, duration) {
        const startTime = performance.now();
        const range = end - start;

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);

            // Ease out cubic
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = start + range * eased;

            element.textContent = `${current.toFixed(1)}%`;

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }

        requestAnimationFrame(update);
    }

    /**
     * Show error toast notification
     */
    function showError(message) {
        errorToast.textContent = `❌ ${message}`;
        errorToast.classList.add('show');

        setTimeout(() => {
            errorToast.classList.remove('show');
        }, 4000);
    }

    // Add subtle focus animations to form inputs
    document.querySelectorAll('.form-input, .form-select').forEach(input => {
        input.addEventListener('focus', () => {
            input.parentElement.style.transform = 'translateY(-1px)';
        });
        input.addEventListener('blur', () => {
            input.parentElement.style.transform = 'translateY(0)';
        });
    });
});
