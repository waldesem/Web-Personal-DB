<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import { classifyStore } from "@/store/classify";
import { profileStore } from "@/store/profile";

const ModalWin = defineAsyncComponent(
  () => import("@components/layouts/ModalWin.vue")
);
const SelectDiv = defineAsyncComponent(
  () => import("@components/elements/SelectDiv.vue")
);

const storeClassify = classifyStore();
const storeProfile = profileStore();
</script>

<template>
  <ModalWin :id="'modalRegion'" :title="'Изменить регион'" :size="'modal-md'">
    <form
      @change.prevent="storeProfile.dataProfile.updateItem"
      class="form form-check"
      role="form"  data-bs-dismiss="modal"
    >
      <SelectDiv
        :name="'region_id'"
        :label="'Регион'"
        :select="storeClassify.classData.regions"
        :model="storeProfile.dataProfile.form['region_id']"
        @input-event="
          storeProfile.dataProfile.form['region_id'] = $event.target.value
        "
      />
    </form>
  </ModalWin>
</template>
