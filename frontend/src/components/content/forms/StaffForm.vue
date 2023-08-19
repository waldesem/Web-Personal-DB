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

  emit('formItem', {
    'position': formData.value['position'], 
    'department': formData.value['department']
  });
}

</script>

<template>
    <form @submit.prevent="submitData" class="form form-check" role="form">
    <div class="mb-3 row required">
        <label class="col-form-label col-lg-2" for="position">Должность</label>
        <div class="col-lg-10">
        <input class="form-control" id="position" maxlength="250" name="position" required type="text" v-model="formData['position']">
        </div>
    </div>
    <div class="mb-3 row">
        <label class="col-form-label col-lg-2" for="department">Деператамент/Кластер</label>
        <div class="col-lg-10">
        <input class="form-control" id="department" maxlength="250" name="department" type="text" v-model="formData['department']">
        </div>
    </div>
    <div class=" row">
        <div class="offset-lg-2 col-lg-10">
            <button class="btn btn-outline-primary btn-md" name="submit" type="submit">Принять</button>
        </div>
    </div>
    </form>
</template>
