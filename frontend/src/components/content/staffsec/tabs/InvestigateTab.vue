<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
import { Inquisition } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);
const InvestigationForm = defineAsyncComponent(
  () => import("../forms/InvestigationForm.vue")
);
const FileForm = defineAsyncComponent(
  () => import("@components/layouts/HeaderDiv.vue")
);

onBeforeMount( async() => {
  await props.getItem("poligraf");
});

const props = defineProps({
  candId: String,
  userId: String,
  inquisitions:  {
    type: Array as () => Inquisition[],
    default: () => {},
  },
  getItem: {
    type: Function,
    required: true,
  },
  updateItem: {
    type: Function,
    required: true,
  },
  deleteItem: {
    type: Function,
    required: true,
  },
  submitFile: {
    type: Function,
    required: true,
  },
});

const inquisition = ref({
  action: "",
  isForm: false,
  itemId: "",
  item: <Inquisition>{},

  getEvent (event: Event){
    props.submitFile(event, 'check')
  },
});
</script>

<template>
  <div class="py-3">
    <template v-if="inquisition.isForm">
    <InvestigationForm
      :get-item="props.getItem"
      :action="inquisition.action"
      :cand-id="candId"
      :content="inquisition.item"
      :update-item="props.updateItem"
      @deactivate="inquisition.isForm = false; inquisition.action = '';"
    />
    </template>
    <div v-else>
      <div v-if="props.inquisitions.length">
        <CollapseDiv
          v-for="(item, idx) in props.inquisitions"
          :key="idx"
          :id="'investigation' + idx"
          :idx="idx"
          :label="'Расследование #' + (idx + 1)"
        >
          <RowDivSlot :slotTwo="true" :print="true">
            <template v-slot:divTwo>
              <a
                href="#"
                title="Удалить"
                @click="props.deleteItem(item['id'].toString())"
              >
                <i class="bi bi-trash"></i>
              </a>
              <a
                href="#"
                title="Изменить"
                @click="
                  inquisition.isForm = true;
                  inquisition.action = 'update';
                  inquisition.item = item;
                  inquisition.itemId = item['id'].toString();
                "
              >
                <i class="bi bi-pencil-square"></i>
              </a>
            </template>
          </RowDivSlot>
          <RowDivSlot :label="'Тема'" :value="item['theme']" />
          <RowDivSlot :label="'Информация'" :value="item['info']" />
          <RowDivSlot :label="'Сотрудник'" :value="item['officer']" />
          <RowDivSlot
            :label="'Дата'"
            :value="new Date(String(item['deadline'])).toLocaleDateString('ru-RU')"
          />
        </CollapseDiv>
        <FileForm
          :accept="'*'"
          @submit="inquisition.getEvent"
        />
      </div>
      <p v-else>Данные отсутствуют</p>
      <div class="d-print-none py-3">
        <a
          class="btn btn-outline-primary"
          type="button"
          @click="
            inquisition.isForm = true;
            inquisition.action = 'create';
          "
          >Добавить запись
        </a>
      </div>
    </div>
  </div>
</template>
