/** @type {import('tailwindcss').Config} */
module.exports = {
	content: ['./core/**/*.{html,js}'],
	theme: {
		variants: {
			extend: {
				backgroundColor: ['hover'],
				textColor: ['hover'],
				// Add other variants as needed
			},
		},
	},
	plugins: [],
}
