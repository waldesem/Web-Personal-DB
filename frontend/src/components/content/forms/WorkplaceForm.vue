<script setup lang="ts">
// компонент для отображения формы добавления и редактирования данных 

import { toRef } from 'vue';

const emit = defineEmits(['formItem']);

const props = defineProps({
    item: {
        type: Object,
        required: true,
        default: () => ({})
    }
});

const formData = toRef(props.item);


 /**
  * Updates or adds an item.
  *
  * @return {void} 
  */
 function submitData(): void {
  emit('formItem', { 'period': formData.value['period'], 'workplace': formData.value['workplace'], 'address': formData.value['address'], 'position': formData.value['position'] });
}

</script>

<template>
   <form @submit.prevent="submitData" class="form form-check" role="form">
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="period">Период работы</label>
        <div class="col-lg-10">
        <input class="form-control" id="period" maxlength="25" name="period" type="text" v-model="formData['period']">
        </div>
    </div>
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="workplace">Место работы</label>
        <div class="col-lg-10">
        <input class="form-control" id="workplace" maxlength="250" name="workplace" required type="text" v-model="formData['workplace']">
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="address">Адрес организации</label>
        <div class="col-lg-10">
        <input class="form-control" id="address" maxlength="250" name="address" type="text" v-model="formData['address']">
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="position">Должность</label>
        <div class="col-lg-10">
        <input class="form-control" id="position" maxlength="250" name="position" type="text" v-model="formData['position']">
        </div>
    </div>
    <div class=" row">
        <div class="offset-lg-2 col-lg-10">
            <button class="btn btn-outline-primary btn-md" name="submit" type="submit">Принять</button>
        </div>
    </div>
    </form>
</template>
