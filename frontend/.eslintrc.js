module.exports = {
  root: true,
  env: {
    node: true,
    browser: true,
    es6: true
  },
  extends: [
    'plugin:vue/essential',
    'eslint:recommended'
  ],
  parserOptions: {
    parser: '@babel/eslint-parser',
    requireConfigFile: false,
    ecmaVersion: 2020,
    sourceType: 'module'
  },
  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    // Vue相关规则
    'vue/multi-word-component-names': 'off',
    'vue/no-v-model-argument': 'off',
    'vue/no-mutating-props': 'warn',
    // 基本规则
    'indent': ['error', 2],
    'quotes': ['error', 'single'],
    'semi': ['error', 'never'],
    'comma-dangle': ['error', 'never'],
    // 允许使用 async-await
    'generator-star-spacing': 'off',
    // 允许 debugger 在开发环境
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    // 关闭命名检查
    'vue/name-property-casing': 'off'
  },
  overrides: [
    {
      files: ['*.vue'],
      rules: {
        'indent': 'off'
      }
    }
  ]
} 