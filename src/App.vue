<style scoped>
.范围 {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  padding: 20px;
}

.范围 input {
  display: block;
  padding: 8px;
  width: 100%;
  height: 6vh;
  max-width: 400px;
  border-radius: 5px;
  border: none;
  margin: 10px auto 20px;
}

.范围 button {
  margin-top: 2vh;
  width: 20vw;
  height: 4vh;
  min-width: 100px;
  background: #b2e3c9;
  border: none;
  border-radius: 40px;
  transition: all 0.3s ease;
}

.范围 button:hover {
  background: #91c5a7;
}

.范围 > div,.答题界面{
  display: flex!important;
  flex-direction: column;
  align-items: center;
}

.范围 > div > div{
  display: grid;
  margin-top: 20px;
  flex-direction: column;
  align-items: center;
}

.首页按钮 {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-row-gap: 10px;
  grid-column-gap: 10px;
  justify-items: center;
}

mdui-button{
  margin-top: 10px;
}

h1{
  margin-bottom: 20px;
}

mdui-linear-progress{
  position: fixed;
  top: 0;
}
@media (max-width: 768px) {
  .首页按钮 {
    grid-template-columns: 1fr;
  }

  .范围 button {
    width: 60vw;
    height: 40px;
  }
}


</style>

<style>

button > p {
  color: black;
}

* {
  margin: 0;
  padding: 0;
}
</style>

<template>
  <div class="范围 mdui-theme-dark">
    <mdui-linear-progress :value="已完成数量/数据源总量"></mdui-linear-progress>
    <!-- 数据输入区域 -->
    <div v-if="!学习模式">
      <h1>Maybe</h1>
      <mdui-card>
        <mdui-text-field @input="新题目 = $event.target.value" label="输入题目（支持Markdown）"/>
        <mdui-text-field @input="新答案 = $event.target.value" label="输入答案（支持Markdown）"/>
      </mdui-card>
      <div class="首页按钮">
        <mdui-button @click="开始学习()">开始学习</mdui-button>
        <mdui-button @click="添加数据源()">添加</mdui-button>
        <mdui-button @click="导出到剪贴板()">导出到剪贴板</mdui-button>
        <mdui-button @click="从剪贴板导入()">导入数据源</mdui-button>
        <mdui-button @click="清空数据源()">清空数据源</mdui-button>
      </div>
    </div>

    <!-- 学习模式 -->
    <div v-else>
      <div v-if="当前题目" class="答题界面">
        <!-- 渲染Markdown题目 -->
        <div v-html="renderMarkdown(当前题目.题目)"></div>

        <!-- 选项按钮 -->
        <mdui-button
          v-for="(选项, 索引) in 选项列表"
          :key="索引"
          @click="处理答案选择(选项)"
          v-html="renderMarkdown(选项)"
        ></mdui-button>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import {onMounted, ref} from 'vue'

// 修改 App.vue 的 import 部分
import MarkdownIt from 'markdown-it'
import markdownItKatex from 'markdown-it-katex'
import 'katex/dist/katex.min.css'

import {type Card, useDataStore} from '@/stores/datastores.ts'
import 'mdui/mdui.css';
import 'mdui';
import {snackbar} from "mdui";
const md = new MarkdownIt({html: true}).use(markdownItKatex)

function renderMarkdown(text: string): string {
  return md.render(text)
}

// 以下保留你原来的逻辑：
const 数据仓库 = useDataStore()
const 新题目 = ref('')
const 新答案 = ref('')
const 学习模式 = ref(false)
const 数据源 = ref<Card[]>(数据仓库.dataSource || [])
let 已完成数量 = ref(0)
let 数据源总量 = ref(1)
const 当前卡片组 = ref<Card[]>([])
const 当前题目 = ref<Card | null>(null)
const 选项列表 = ref<string[]>([])

onMounted(() => {
  载入数据()
})

function 载入数据() {
  const 保存数据 = localStorage.getItem('dataSource')
  if (保存数据) {
    const 解析后 = JSON.parse(保存数据) as Card[]
    数据源.value = 解析后
    数据仓库.setDataSource(解析后)
  }
}

function 保存到本地存储() {
  localStorage.setItem('dataSource', JSON.stringify(数据源.value))
  数据仓库.setDataSource(数据源.value)
}

function 清空数据源() {
  if (confirm('确定要清空数据源吗？')) {
    数据源.value = []
    保存到本地存储()
    snackbar({
      message: '数据已清空',
    })
  }
}


function 添加数据源() {
  console.log(新题目,新答案)
  if (新题目.value && 新答案.value) {
    const 新项目: Card = {
      题目: 新题目.value,
      答案: 新答案.value,
      记忆标记: 1
    }
    保存到本地存储()
    数据源.value.push(新项目)
    新题目.value = ''
    新答案.value = ''
  }
}

async function 导出到剪贴板() {
  try {
    await navigator.clipboard.writeText(JSON.stringify(数据源.value))
    alert('数据源已复制到剪贴板')
  } catch (错误) {
    console.error('复制失败:', 错误)
  }
}

async function 从剪贴板导入() {
  try {
    const 文本 = await navigator.clipboard.readText()
    const 数据 = JSON.parse(文本) as Partial<Card>[]

    // 数据清洗与默认值填充
    const 清洗后数据 = 数据
      .filter(item => item.题目 && item.答案)
      .map(item => ({
        题目: item.题目!,
        答案: item.答案!,
        记忆标记: typeof item.记忆标记 === 'number' ? item.记忆标记 : 3
      }))

    if (清洗后数据.length === 0) {
      throw new Error('数据中没有有效卡片')
    }

    数据源.value = 清洗后数据 as Card[]
    保存到本地存储()
    开始学习()
    snackbar({
      message: '导入成功',
    })
  } catch (错误) {
    console.error('导入失败:', 错误)
    alert(`导入失败: ${错误}`)
  }
}


function 开始学习() {
  if (数据源.value.length === 0) {
    alert('请先添加题目')
    return
  }
  已完成数量.value = 1
  数据源总量.value = 数据源.value.length
  学习模式.value = true
  重置学习状态()
}

function 生成选项() {
  if (当前卡片组.value.length === 0) return

  // 从localStorage直接读取最新数据
  const 保存数据 = localStorage.getItem('dataSource')
  const 数据源本地 = 保存数据 ? JSON.parse(保存数据) : []

  当前题目.value = 当前卡片组.value[0]
  const 正确答案 = 当前题目.value.答案

  // 使用localStorage中的数据源
  const 其他选项 = 数据源本地
    .filter((项目: Card) => 项目.答案 !== 正确答案)
    .map((项目: Card) => 项目.答案)
    .sort(() => 0.5 - Math.random())
    .slice(0, 3)

  选项列表.value = [正确答案, ...其他选项].sort(() => 0.5 - Math.random())
}


function 重置学习状态() {
  当前卡片组.value = 数据源.value
  生成选项()
}

function 处理答案选择(选择的答案: string) {
  if (!当前题目.value) return
  const 当前卡片 = 当前卡片组.value[0]
  const 是否正确 = 选择的答案 === 当前卡片.答案
  if (是否正确) {
    当前卡片.记忆标记 = (当前卡片.记忆标记 || 3) - 1
    if (当前卡片.记忆标记 <= 0) {
      已完成数量.value+=1
      当前卡片组.value.shift()
    } else {
      当前卡片组.value.push(当前卡片组.value.shift()!)
    }
  } else {
    alert('答案错误！')
    if (当前卡片.记忆标记!==undefined && 当前卡片.记忆标记 + 1 <= 3) {
      当前卡片.记忆标记++
    }
    当前卡片组.value.push(当前卡片组.value.shift()!)
  }
  if (当前卡片组.value.length === 0) {
    alert('所有卡片已完成！')
    载入数据()
    学习模式.value = false
    数据源总量.value = 1
    已完成数量.value = 0
  }
  生成选项()
}
</script>

