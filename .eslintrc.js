module.exports = {
    env: {
        es2020: true,
        node: true,
        browser: true
    },
    extends: [
        'eslint:recommended'
    ],
    parserOptions: {
        ecmaVersion: 11,
        sourceType: 'module'
    },
    rules: {
        'no-multiple-empty-lines': 'warn',
        'no-var': 'error',
        'prefer-const': 'error',
        'comma-dangle': 0,
        'indent': ['error', 4],
    }
};
