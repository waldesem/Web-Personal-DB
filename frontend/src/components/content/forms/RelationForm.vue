<script setup lang="ts">
// компонент для отображения формы добавления и редактирования данных 
 
import { appAnketa } from '@/store/anketa';

const storeAnketa = appAnketa();

</script>

<template>
   <form @submit.prevent="storeAnketa.updateItem" class="form form-check" role="form">
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="relation">Тип связи</label>
        <div class="col-lg-10">
        <input class="form-control" id="relation" maxlength="250" name="relation" type="text" v-model="storeAnketa.itemForm['relation']">
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="relation_id">ID связи</label>
        <div class="col-lg-10">
        <input class="form-control" id="relation_id" maxlength="25" name="relation_id" type="text" v-model="storeAnketa.itemForm['relation_id']">
        </div>
    </div>
    <div class=" row">
        <div class="offset-lg-2 col-lg-10">
            <button class="btn btn-outline-primary btn-md" name="submit" type="submit">Принять</button>
        </div>
    </div>
    </form>
</template>
