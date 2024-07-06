Vue.component("feedback-form", {
	data() {
		return {
			score: 0,
			isLoading: false,
			isError: false,
			isDone: false,
		};
	},
	template: "#feedback-form",
	methods: {
		async submitFeedback() {
			try {
				this.isLoading = true;
				await axios.post("http://localhost:8000/feedback/", {
					score: this.score,
				});
				this.isDone = true;
				// alert("Feedback submitted successfully");
			} catch (error) {
				// alert("Failed to submit feedback");
				this.isError = true;
			} finally {
				this.isLoading = false;
			}
		},
	},
});

new Vue({
	el: "#app",
});
