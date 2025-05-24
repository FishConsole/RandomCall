import { defineStore } from 'pinia'

export interface Card {
  题目: string
  答案: string
  记忆标记?: number
}

export const useDataStore = defineStore('dataStore', {
  state: () => ({
    dataSource: [] as Card[]
  }),
  actions: {
    setDataSource(data: Card[]) {
      this.dataSource = data
    }
  }
})
