import js from "@eslint/js";
import globals from "globals";
import nextPlugin from "@next/eslint-plugin-next";
import reactPlugin from "eslint-plugin-react";
import hooksPlugin from "eslint-plugin-react-hooks";

export default [
    js.configs.recommended,
    {
        files: ["**/*.{js,mjs,cjs,jsx,mjsx,ts,tsx,mtsx}"],
        plugins: {
            "@next/next": nextPlugin,
            react: reactPlugin,
            "react-hooks": hooksPlugin,
        },
        languageOptions: {
            ecmaVersion: "latest",
            sourceType: "module",
            globals: {
                ...globals.browser,
                ...globals.node,
            },
            parserOptions: {
                ecmaFeatures: {
                    jsx: true,
                },
            },
        },
        settings: {
            react: {
                version: "detect",
            },
        },
        rules: {
            // Base React & Next.js Recommended Rules
            ...reactPlugin.configs.recommended.rules,
            ...hooksPlugin.configs.recommended.rules,
            ...nextPlugin.configs.recommended.rules,
            ...nextPlugin.configs["core-web-vitals"].rules,

            // Code Quality & Best Practices
            "eqeqeq": ["error", "always"],                   // Enforce strict equality (=== / !==)
            "no-var": "error",                               // Disallow legacy var keywords
            "prefer-const": "error",                         // Require const for variables never reassigned
            "curly": ["error", "all"],                       // Require curly braces for all control statements
            "no-console": ["warn", { allow: ["warn", "error"] }], // Flag leftover console.log statements
            "no-duplicate-imports": "error",                 // Disallow duplicate module imports
            "no-unused-vars": ["warn", { argsIgnorePattern: "^_", varsIgnorePattern: "^_" }],

            // React Specific Best Practices & Style Rules
            "react/react-in-jsx-scope": "off",               // Not needed in Next.js / React 17+
            "react/prop-types": "off",                       // Not required
            "react/self-closing-comp": "error",              // Enforce self-closing tags for elements without children
            "react/jsx-no-useless-fragment": "error",        // Disallow unnecessary React fragments
            "react-hooks/rules-of-hooks": "error",          // Enforce React Hook rules
            "react-hooks/exhaustive-deps": "warn",           // Enforce effect dependencies
        },
    },
];