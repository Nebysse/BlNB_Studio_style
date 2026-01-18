'use client'

import { useEffect, useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { Folder, File, ArrowUp, RefreshCw, Settings, Film } from 'lucide-react'

interface ProjectState {
  filepath?: string
  filename?: string
  project_root?: string
  metadata?: any
  object_count?: number
  scenes?: string[]
}

interface ProjectInfo {
  project_root?: string
  metadata?: {
    project?: {
      code?: string
      type?: string
    }
    author?: {
      name?: string
      studio?: string
    }
  }
  filepath?: string
  filename?: string
  object_count?: number
}

interface FileItem {
  name: string
  path: string
  is_dir: boolean
  size: number
}

export default function Home() {
  const [projectState, setProjectState] = useState<ProjectState | null>(null)
  const [projectInfo, setProjectInfo] = useState<ProjectInfo | null>(null)
  const [files, setFiles] = useState<FileItem[]>([])
  const [currentPath, setCurrentPath] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [initResult, setInitResult] = useState<{ type: 'success' | 'error' | 'loading'; message: string } | null>(null)
  const [initForm, setInitForm] = useState({
    base_path: '',
    project_code: '',
    project_type: 'single_shot',
    author_name: '',
    studio: ''
  })

  const loadProjectState = async () => {
    try {
      const res = await fetch('/api/project/state')
      const data = await res.json()
      setProjectState(data)
    } catch (e) {
      console.error('加载项目状态失败:', e)
    }
  }

  const loadProjectInfo = async () => {
    try {
      const res = await fetch('/api/project/info')
      if (res.ok) {
        const data = await res.json()
        setProjectInfo(data)
        setError(null)
      } else {
        const data = await res.json()
        setError(data.error || '未找到项目')
      }
    } catch (e: any) {
      setError('加载项目信息失败: ' + e.message)
    } finally {
      setLoading(false)
    }
  }

  const loadFiles = async (path = '') => {
    try {
      const url = path ? `/api/files/list?path=${encodeURIComponent(path)}` : '/api/files/list'
      const res = await fetch(url)
      if (res.ok) {
        const data = await res.json()
        setFiles(data.files || [])
        setCurrentPath(data.path || '')
      }
    } catch (e) {
      console.error('加载文件列表失败:', e)
    }
  }

  useEffect(() => {
    loadProjectState()
    loadProjectInfo()
    loadFiles()
    
    const interval = setInterval(() => {
      loadProjectState()
      loadProjectInfo()
    }, 2000)
    
    return () => clearInterval(interval)
  }, [])

  const handleFileClick = (file: FileItem) => {
    if (file.is_dir) {
      loadFiles(file.path)
    }
  }

  const navigateUp = () => {
    if (currentPath) {
      const parts = currentPath.split('/').filter(p => p)
      parts.pop()
      loadFiles(parts.join('/'))
    }
  }

  const handleInitSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setInitResult({ type: 'loading', message: '初始化中...' })
    
    try {
      const res = await fetch('/api/project/init', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(initForm)
      })
      const data = await res.json()
      
      if (data.success) {
        setInitResult({ type: 'success', message: `项目初始化成功: ${data.project_root}` })
        setTimeout(() => {
          loadProjectInfo()
          loadFiles()
        }, 500)
      } else {
        setInitResult({ type: 'error', message: data.error || '初始化失败' })
      }
    } catch (e: any) {
      setInitResult({ type: 'error', message: '初始化失败: ' + e.message })
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto p-6 max-w-7xl">
        <h1 className="text-4xl font-bold text-primary mb-8 flex items-center gap-3">
          <Film className="w-10 h-10" />
          Blender Studio 项目管理
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span className="flex items-center gap-2">
                  <Folder className="w-5 h-5" />
                  项目信息
                </span>
                {projectState?.project_root && (
                  <Badge className="bg-primary">已连接</Badge>
                )}
              </CardTitle>
            </CardHeader>
            <CardContent>
              {loading && !projectInfo ? (
                <div className="text-center py-8 text-muted-foreground">加载中...</div>
              ) : error ? (
                <div className="text-destructive bg-destructive/10 p-4 rounded-lg">{error}</div>
              ) : projectInfo ? (
                <div className="space-y-4">
                  <div>
                    <Label className="text-muted-foreground text-sm">项目根目录</Label>
                    <p className="text-sm mt-1 break-all">{projectInfo.project_root || 'N/A'}</p>
                  </div>
                  <div>
                    <Label className="text-muted-foreground text-sm">项目代号</Label>
                    <p className="mt-1">{projectInfo.metadata?.project?.code || 'N/A'}</p>
                  </div>
                  <div>
                    <Label className="text-muted-foreground text-sm">项目类型</Label>
                    <p className="mt-1">{projectInfo.metadata?.project?.type || 'N/A'}</p>
                  </div>
                  <div>
                    <Label className="text-muted-foreground text-sm">作者</Label>
                    <p className="mt-1">{projectInfo.metadata?.author?.name || 'N/A'}</p>
                  </div>
                  <div>
                    <Label className="text-muted-foreground text-sm">工作室</Label>
                    <p className="mt-1">{projectInfo.metadata?.author?.studio || 'N/A'}</p>
                  </div>
                  {projectState?.filename && (
                    <div>
                      <Label className="text-muted-foreground text-sm">当前文件</Label>
                      <p className="mt-1 text-secondary">{projectState.filename}</p>
                    </div>
                  )}
                  {projectState?.object_count !== undefined && (
                    <div>
                      <Label className="text-muted-foreground text-sm">对象数量</Label>
                      <p className="mt-1">{projectState.object_count}</p>
                    </div>
                  )}
                </div>
              ) : null}
              <Button onClick={loadProjectInfo} className="mt-4 w-full" variant="outline">
                <RefreshCw className="w-4 h-4 mr-2" />
                刷新
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Film className="w-5 h-5" />
                Blender 文件信息
              </CardTitle>
            </CardHeader>
            <CardContent>
              {projectState?.filepath ? (
                <div className="space-y-4">
                  <div>
                    <Label className="text-muted-foreground text-sm">文件路径</Label>
                    <p className="text-xs mt-1 break-all text-muted-foreground">{projectState.filepath}</p>
                  </div>
                  <div>
                    <Label className="text-muted-foreground text-sm">文件名</Label>
                    <p className="mt-1">{projectState.filename}</p>
                  </div>
                </div>
              ) : (
                <div className="text-center py-8 text-muted-foreground">未打开文件</div>
              )}
              <Button onClick={loadProjectState} className="mt-4 w-full" variant="outline">
                <RefreshCw className="w-4 h-4 mr-2" />
                刷新
              </Button>
            </CardContent>
          </Card>
        </div>

        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Folder className="w-5 h-5" />
              文件浏览器
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-4 mb-4">
              <Button onClick={navigateUp} disabled={!currentPath} variant="secondary" size="sm">
                <ArrowUp className="w-4 h-4 mr-2" />
                上一级
              </Button>
              <span className="text-sm text-muted-foreground">/{currentPath || '根目录'}</span>
            </div>
            <div className="space-y-1">
              {files.length === 0 ? (
                <div className="text-center py-8 text-muted-foreground">目录为空</div>
              ) : (
                files.map((file, idx) => (
                  <div
                    key={idx}
                    className="flex items-center gap-3 p-3 rounded-lg hover:bg-accent cursor-pointer transition-colors"
                    onClick={() => handleFileClick(file)}
                  >
                    {file.is_dir ? (
                      <Folder className="w-5 h-5 text-primary" />
                    ) : (
                      <File className="w-5 h-5 text-muted-foreground" />
                    )}
                    <span className="flex-1">{file.name}</span>
                    {!file.is_dir && (
                      <span className="text-xs text-muted-foreground">
                        {(file.size / 1024).toFixed(2)} KB
                      </span>
                    )}
                  </div>
                ))
              )}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Settings className="w-5 h-5" />
              初始化项目
            </CardTitle>
          </CardHeader>
          <CardContent>
            {initResult && (
              <div className={`mb-4 p-4 rounded-lg ${
                initResult.type === 'success' 
                  ? 'bg-green-500/10 text-green-500' 
                  : initResult.type === 'error'
                  ? 'bg-destructive/10 text-destructive'
                  : 'text-muted-foreground'
              }`}>
                {initResult.message}
              </div>
            )}
            <form onSubmit={handleInitSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label>项目根目录</Label>
                <Input
                  value={initForm.base_path}
                  onChange={(e) => setInitForm({...initForm, base_path: e.target.value})}
                  placeholder="例如: C:\projects"
                />
              </div>
              <div className="space-y-2">
                <Label>项目代号</Label>
                <Input
                  value={initForm.project_code}
                  onChange={(e) => setInitForm({...initForm, project_code: e.target.value})}
                  placeholder="例如: wing_it"
                />
              </div>
              <div className="space-y-2">
                <Label>项目类型</Label>
                <Select value={initForm.project_type} onValueChange={(value) => setInitForm({...initForm, project_type: value})}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="single_shot">单镜头练习</SelectItem>
                    <SelectItem value="short_film">多镜头短片</SelectItem>
                    <SelectItem value="asset_library">资产库项目</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <Label>作者名称</Label>
                <Input
                  value={initForm.author_name}
                  onChange={(e) => setInitForm({...initForm, author_name: e.target.value})}
                />
              </div>
              <div className="space-y-2">
                <Label>工作室</Label>
                <Input
                  value={initForm.studio}
                  onChange={(e) => setInitForm({...initForm, studio: e.target.value})}
                />
              </div>
              <Button type="submit" className="w-full">初始化项目</Button>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
