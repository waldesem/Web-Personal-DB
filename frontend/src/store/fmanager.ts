import { defineStore } from 'pinia'
import { ref } from 'vue';

export const fileManagerStore = defineStore('fileManagerStore', () => {

  const fileManager = ref({
    path: Array<string>(),
    folders: Array<string>(),
    files: Array<string>(),
    action: '',
    select: false,
    selected: Array<string>(),
    copied: Array<string>(),
  });

  return {
    fileManager
    }
});
