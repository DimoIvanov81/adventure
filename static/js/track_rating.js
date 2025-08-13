// CSRF cookie helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {
    const ratingBox = document.getElementById('star-rating');
    if (!ratingBox) return;

    const stars = ratingBox.querySelectorAll('.star');
    const rateUrl = ratingBox.dataset.rateUrl;
    if (!rateUrl || stars.length === 0) return;

    const averageRatingSpan = document.getElementById('average-rating');
    const ratingCountSpan = document.getElementById('rating-count');

    function updateStarsDisplay(rating) {
        stars.forEach(star => star.classList.remove('rated', 'half'));

        stars.forEach((star, i) => {
            if (rating >= i + 1) {
                star.classList.add('rated'); // пълна
            } else if (rating > i && rating < i + 1) {
                star.classList.add('half'); // половинка
            }
        });
    }


    // покажи гласа на потребителя при зареждане
    const initialUserRating = parseFloat(ratingBox.dataset.userRating) || 0;
    updateStarsDisplay(initialUserRating);

    stars.forEach(star => {
        star.addEventListener('click', function () {
            const selectedRating = this.dataset.value;

            fetch(rateUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({rating: selectedRating})
            })
                .then(response => {
                    if (!response.ok) throw new Error('Error submitting rating.');
                    return response.json();
                })
                .then(data => {
                    // визуализирай по НОВАТА средна оценка
                    updateStarsDisplay(data.average_rating);

                    if (averageRatingSpan) averageRatingSpan.textContent = Number(data.average_rating).toFixed(1);
                    if (ratingCountSpan) ratingCountSpan.textContent = data.ratings_count;
                })
                .catch(err => console.error('Rating error:', err));
        });

        star.addEventListener('mouseenter', function () {
            const value = parseInt(this.dataset.value);
            stars.forEach((s, i) => s.classList.toggle('hovered', i < value));
        });

        star.addEventListener('mouseleave', function () {
            stars.forEach(s => s.classList.remove('hovered'));
        });
    });
});
