Vue.component("feedback-form", {
	data() {
		return {
			score: 0, // The score to be submitted in the feedback form
			isLoading: false, // Indicates if the form is currently submitting
			isError: false, // Indicates if there was an error during submission
			isDone: false, // Indicates if the form was successfully submitted
			isClose: false, // Indicates if the form should be closed
		};
	},
	template: "#feedback-form",
	methods: {
		/**
		 * Resets the state of the feedback form.
		 * This method sets all status flags to false.
		 */
		resetState() {
			this.isLoading = false;
			this.isError = false;
			this.isDone = false;
			this.isClose = false;
		},

		/**
		 * Submits the feedback score to the server.
		 * This method sends a POST request to the /feedback endpoint with the score.
		 * It also handles the form's loading, success, and error states.
		 */
		async submitFeedback() {
			this.resetState(); // Reset form state before submission
			try {
				this.isLoading = true; // Set loading state to true
				// Send POST request to /feedback with the score
				await axios.post("/feedback", {
					score: this.score,
				});
				this.isDone = true; // Set done state to true upon successful submission
				// Set close state to true after 500ms to close the form
				setTimeout(() => {
					this.isClose = true;
				}, 500);
			} catch (error) {
				this.isError = true; // Set error state to true if submission fails
			} finally {
				this.isLoading = false; // Reset loading state after submission attempt
			}
		},
	},
});

// Initialize the Vue instance
new Vue({
	el: "#app",
});
