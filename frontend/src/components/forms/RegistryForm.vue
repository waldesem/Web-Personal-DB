<script setup lang="ts">

import { profileStore } from '@/store/profile';
import { classifyStore } from '@/store/classify';

const storeClassify = classifyStore();
const storeProfile = profileStore();

</script>

<template v-if="storeProfile.action === 'create' && storeProfile.flag === 'registry'">
    <form @submit.prevent="storeProfile.updateItem()" class="form form-check" role="form">
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="comments">Комментарий</label>
        <div class="col-lg-10">
          <textarea class="form-control" id="comments" name="comments" 
                    v-model="storeProfile.itemForm['comments']"></textarea>
        </div>
      </div>
      <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="decision">Решение</label>
        <div class="col-lg-10">
          <select class="form-select" id="decision" name="decision" 
                  v-model="storeProfile.itemForm['decision']">
            <option v-for="(name, value) in storeClassify.classifyItems.decision" 
                    :key="value" :value="name">
                    {{ name }}
            </option>
          </select>
        </div>
      </div>
      <div class=" row">
        <div class="offset-lg-2 col-lg-10">
          <div class="btn-group" role="group" :disabled="storeProfile.spinner">              
            <button class="btn btn-outline-primary" type="submit">
                {{ !storeProfile.spinner ? 'Принять' : '' }}
              <span v-if="storeProfile.spinner" class="spinner-border spinner-border-sm" 
                    aria-hidden="true"></span>
              <span v-if="storeProfile.spinner" role="status">Отправляется...</span>
            </button>
            <button v-if="!storeProfile.spinner" class="btn btn-outline-primary" 
                    type="reset">Очистить</button>
            <button v-if="!storeProfile.spinner" class="btn btn-outline-primary" 
                    type="button" @click="storeProfile.cancelEdit">Отмена</button>
          </div>
        </div>
      </div>
    </form>
  </template>