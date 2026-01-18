import type { Config } from "tailwindcss"

const config = {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  prefix: "",
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(0 0% 14.9%)",
        input: "hsl(0 0% 14.9%)",
        ring: "hsl(24.6 95% 53.1%)",
        background: "hsl(0 0% 10%)",
        foreground: "hsl(0 0% 88%)",
        primary: {
          DEFAULT: "hsl(24.6 95% 53.1%)",
          foreground: "hsl(0 0% 98%)",
        },
        secondary: {
          DEFAULT: "hsl(210 100% 56.1%)",
          foreground: "hsl(0 0% 98%)",
        },
        destructive: {
          DEFAULT: "hsl(0 62.8% 30.6%)",
          foreground: "hsl(0 0% 98%)",
        },
        muted: {
          DEFAULT: "hsl(0 0% 18%)",
          foreground: "hsl(0 0% 63.9%)",
        },
        accent: {
          DEFAULT: "hsl(0 0% 18%)",
          foreground: "hsl(0 0% 98%)",
        },
        card: {
          DEFAULT: "hsl(0 0% 18%)",
          foreground: "hsl(0 0% 88%)",
        },
      },
      borderRadius: {
        lg: "0.5rem",
        md: "calc(0.5rem - 2px)",
        sm: "calc(0.5rem - 4px)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
} satisfies Config

export default config
