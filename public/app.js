Vue.component("feedback-form", {
	data() {
		return {
			score: 0,
			isLoading: false,
			isError: false,
			isDone: false,
			isClose: false,
		};
	},
	template: "#feedback-form",
	methods: {
		resetState() {
			this.score = 0;
			this.isLoading = false;
			this.isError = false;
			this.isDone = false;
			this.isClose = false;
		},
		async submitFeedback() {
			this.resetState();
			try {
				this.isLoading = true;
				await axios.post("/feedback", {
					score: this.score,
				});
				this.isDone = true;
				setTimeout(() => {
					this.isClose = true;
				}, 1500);
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
