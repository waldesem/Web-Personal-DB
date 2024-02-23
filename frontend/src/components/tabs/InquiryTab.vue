<script setup lang="ts">
import { defineAsyncComponent } from "vue";
import { profileStore } from "@/store/profile";

const InquiryForm = defineAsyncComponent(
  () => import("@components/forms/InquiryForm.vue")
);
const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);

const storeProfile = profileStore();
</script>

<template>
  <div class="py-3">
    <InquiryForm
      v-if="
        (storeProfile.dataProfile.action === 'update' ||
          storeProfile.dataProfile.action === 'create') &&
        storeProfile.dataProfile.flag === 'inquiry'
      "
    />

    <div v-else>
      <div v-if="storeProfile.dataProfile.needs.length">
        <CollapseDiv
          v-for="(item, idx) in storeProfile.dataProfile.needs"
          :key="idx"
          :id="'inquiry' + idx"
          :idx="idx"
          :label="'Запрос #' + (idx + 1)"
        >
          <RowDivSlot :slotTwo="true" :print="true">
            <template v-slot:divTwo>
              <a
                href="#"
                title="Удалить"
                @click="
                  storeProfile.dataProfile.deleteItem(
                    'inquiry',
                    props.item['id'].toString()
                  )
                "
              >
                <i class="bi bi-trash"></i> </a
              >&nbsp; &nbsp; &nbsp;
              <a
                href="#"
                title="Изменить"
                @click="
                  storeProfile.dataProfile.openForm(
                    'inquiry',
                    'update',
                    props.item['id'].toString(),
                    props.item
                  )
                "
              >
                <i class="bi bi-pencil-square"></i>
              </a>
            </template>
          </RowDivSlot>
          <RowDivSlot :label="'Информация'" :value="props.item['info']" />
          <RowDivSlot :label="'Иннициатор'" :value="props.item['initiator']" />
          <RowDivSlot :label="'Источник'" :value="props.item['source']" />
          <RowDivSlot :label="'Сотрудник'" :value="props.item['officer']" />
          <RowDivSlot :label="'Дата запроса'" :value="props.item['deadline']" />
        </CollapseDiv>
      </div>
      <p v-else>Данные отсутствуют</p>
      <div class="d-print-none py-3">
        <a
          class="btn btn-outline-primary"
          type="button"
          @click="storeProfile.dataProfile.openForm('inquiry', 'create')"
          >Добавить запись
        </a>
      </div>
    </div>
  </div>
</template>
