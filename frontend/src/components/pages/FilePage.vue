<script setup lang="ts">

import { onBeforeMount, defineAsyncComponent } from 'vue';
import { fileManagerStore } from '@store/fmanager';

const ModalWin = defineAsyncComponent(() => import('@components/layouts/ModalWin.vue'));
const HeaderDiv = defineAsyncComponent(() => import('@components/layouts/HeaderDiv.vue'));

const storeFileManager = fileManagerStore();

onBeforeMount(() => {
  storeFileManager.openFolder('');  
});

</script>

<template>
  <div class="container py-3">
    
    <HeaderDiv page-header="Файловый менеджер" />

    <div class="border border-primary p-5" id="fileManager">

      <div class="row border border-primary p-3">
        <div class="col-1">
          <button type="button" class="btn btn-outline-primary" 
            @click="storeFileManager.getFoldersFiles" >
            <i class="bi bi-house" title="Дом"></i>
          </button>
        </div>

        <div class="col-1">
          <button type="button" class="btn btn-outline-primary" 
            @click="storeFileManager.fileManager.action = 'create'; 
                    storeFileManager.updateItem()"
            :disabled="storeFileManager.fileManager.select">
            <i class="bi bi-plus-square" title="Создать"></i>
          </button>
        </div>

        <div class="col-1">
          <button type="button" class="btn btn-outline-primary"
                  @click="storeFileManager.fileManager.select = !storeFileManager.fileManager.select;
                  storeFileManager.fileManager.selected = []">
            <i class="bi bi-check-square" title="Выбрать"></i>
          </button>
        </div>

        <div class="col-1">
          <button type="button" class="btn btn-outline-primary"
                  @click="storeFileManager.fileManager.action = 'copy'; 
                          storeFileManager.fileManager.copied = storeFileManager.fileManager.path;
                          storeFileManager.fileManager.select = false"
                  :disabled="!storeFileManager.fileManager.select || storeFileManager.fileManager.selected.length === 0">
            <i class="bi bi-clipboard" title="Копировать"></i>
          </button>
        </div>

        <div class="col-1">
          <button type="button" class="btn btn-outline-primary"
                  @click="storeFileManager.fileManager.action = 'сut'; 
                          storeFileManager.fileManager.copied = storeFileManager.fileManager.path;
                          storeFileManager.fileManager.select = false"
                  :disabled="!storeFileManager.fileManager.select || storeFileManager.fileManager.selected.length === 0">
            <i class="bi bi-scissors" title="Вырезать"></i>
          </button>
        </div>
          
        <div class="col-1">
          <button type="button" class="btn btn-outline-primary"
                  :disabled="storeFileManager.fileManager.select || storeFileManager.fileManager.selected.length === 0"
                  @click="storeFileManager.copyItem">
            <i class="bi bi-clipboard-fill" title="Вставить"></i>
          </button>
        </div>
          
        <div class="col-1">
          <button type="button" class="btn btn-outline-primary" 
                  @click="storeFileManager.fileManager.action = 'rename'"
                  :disabled="!storeFileManager.fileManager.select || storeFileManager.fileManager.selected.length !== 1"
                  data-bs-toggle="modal" data-bs-target="#modalFile">
            <i class="bi bi-pencil" title="Переменовать"></i>
          </button>
        </div>
          
        <div class="col-1">
          <button type="button" class="btn btn-outline-primary"
                  :disabled="!storeFileManager.fileManager.select || storeFileManager.fileManager.selected.length === 0"
                  @click="storeFileManager.deleteItem">
            <i class="bi bi-trash" title="Удалить"></i>
          </button>
        </div>
      </div>
    
      <div class="py-3">
        <nav aria-label="breadcrumb" :disabled="storeFileManager.fileManager.select">
          <ol class="breadcrumb">
            <li class="breadcrumb-item active" aria-current="page" 
                v-for="item, idx in storeFileManager.fileManager.path" :key="item">
              <a href="#" @click="storeFileManager.fileManager.path = storeFileManager.fileManager.path.slice(0, idx); 
                                  storeFileManager.openFolder(item)">
                {{ item }}
              </a>
            </li>
          </ol>
        </nav>
      </div>

      <ul class="list-group">

        <li class="list-group-item" v-if="storeFileManager.fileManager.path.length">
          <button type="button" href="#" class="list-group-item list-group-item-action" title="Наверх"
                  @click="storeFileManager.fileManager.path = storeFileManager.fileManager.path.slice(0, -1); 
                          storeFileManager.openParent()"
                  :disabled="storeFileManager.fileManager.select">
            <i class="bi bi-arrow-90deg-up"></i>
          </button>
        </li>

        <li class="list-group-item" v-for="folder in storeFileManager.fileManager.folders" :key="folder">
          <div class="item-wrapper fs-6">
            <input class="form-check-input" type="checkbox" v-if="storeFileManager.fileManager.select" 
                  :value="folder" v-model="storeFileManager.fileManager.selected">
            &nbsp;
            <button type="button" class="list-group-item list-group-item-action btn btn-light" 
                    @click="storeFileManager.openFolder(folder)"
                    :disabled="storeFileManager.fileManager.select">
              <i class="bi bi-folder"></i>
              {{ folder }}
            </button>
          </div>
        </li>

        <li class="list-group-item" v-for="file in storeFileManager.fileManager.files" :key="file">
          <div class="item-wrapper">
            <input class="form-check-input" type="checkbox" v-if="storeFileManager.fileManager.select"
                  :value="file" v-model="storeFileManager.fileManager.selected">
            &nbsp; &nbsp;
            <button type="button" class="list-group-item list-group-item-action btn btn-light" 
                    @click="storeFileManager.openFile(file)"
                    :disabled="storeFileManager.fileManager.select">
              <i class="bi bi-file"></i>
              {{ file }}
            </button>
          </div>
        </li>

      </ul>
    </div>
    <modal-win :id="'modalFile'" :title ="'Переменовать'" :size="'modal-md'">
      <template v-slot:body>
        <form @submit.prevent="storeFileManager.updateItem" class="form form-check" role="form">
          <div class="row">
            <div class="col">
              <input class="form-control" id="name" maxlength="250" name="name" type="text"
              v-model="storeFileManager.modalValue">
            </div>
            <div class="col">
              <button class="btn btn-primary btn-md" data-bs-dismiss="modal" name="submit" type="submit">
                Принять
              </button>
            </div>
          </div>
        </form>
      </template>
    </modal-win>
  </div>
</template>

<style scoped>

#fileManager {
  height: 75vh;
  max-height: 75vh;
  overflow-y: auto;
}
.list-group-item .item-wrapper {
  display: flex;
  align-items: center;
}
</style>