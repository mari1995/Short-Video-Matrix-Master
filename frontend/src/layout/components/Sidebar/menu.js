export const menuItems = [
  {
    title: '首页',
    icon: 'el-icon-s-home',
    path: '/dashboard'
  },
  {
    title: '配置中心',
    icon: 'el-icon-setting',
    path: '/settings'
  },
  {
    title: '工具箱',
    icon: 'el-icon-s-tools',
    children: [
      {
        title: 'YouTube下载器',
        icon: 'el-icon-video-play',
        path: '/youtube'
      },
      {
        title: '文件管理',
        icon: 'el-icon-folder',
        path: '/files'
      }
    ]
  },
  {
    title: '视频分析',
    icon: 'el-icon-film',
    path: '/video-analysis'
  }
];

export default menuItems; 