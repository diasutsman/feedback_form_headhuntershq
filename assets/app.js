Vue.component('feedback-form', {
    data() {
        return {
            score: 0
        };
    },
    template: `
        <div>
            <h2>How would you rate your satisfaction with our product?</h2>
            <div v-for="n in 5" :key="n" @click="score = n">
                <span :class="{'selected': n <= score}">★</span>
            </div>
            <button @click="submitFeedback">Submit</button>
        </div>
    `,
    methods: {
        async submitFeedback() {
            try {
                await axios.post('http://localhost:8000/feedback/', { score: this.score });
                alert('Feedback submitted successfully');
            } catch (error) {
                alert('Failed to submit feedback');
            }
        }
    }
});

new Vue({
    el: '#app'
});
