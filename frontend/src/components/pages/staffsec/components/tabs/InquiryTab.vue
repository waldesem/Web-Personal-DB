<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
import { Needs } from "@/interfaces/interface";

const InquiryForm = defineAsyncComponent(
  () => import("@components/pages/staffsec/components/forms/InquiryForm.vue")
);
const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);

onBeforeMount( async() => {
  await props.getItem("poligraf");
});

const props = defineProps({
  candId: String,
  userId: String,
  needs:  {
    type: Array as () => Needs[],
    default: () => {},
  },
  getItem: {
    type: Function,
    required: true,
  },
  deleteItem: {
    type: Function,
    required: true,
  },
  updateItem: {
    type: Function,
    required: true,
  },
  submitFile: {
    type: Function,
    required: true,
  },
});

const need = ref({
  action: "",
  isForm: false,
  itemId: "",
  item: <Needs>{},
});
</script>

<template>
  <div class="py-3">
    <template v-if="need.isForm">
    <InquiryForm
      :get-item="props.getItem"
      :action="need.action"
      :cand-id="candId"
      :content="need.item"
      :update-item="props.updateItem"
      @deactivate="need.isForm = false; need.action = '';"
    />
    </template>
    <div v-else>
      <div v-if="props.needs.length">
        <CollapseDiv
          v-for="(item, idx) in props.needs"
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
                @click="props.deleteItem(item['id'].toString())"
              >
                <i class="bi bi-trash"></i>
              </a>
              <a
                href="#"
                title="Изменить"
                @click="
                  need.isForm = true;
                  need.action = 'update';
                  need.item = item;
                  need.itemId = item['id'].toString();
                "
              >
                <i class="bi bi-pencil-square"></i>
              </a>
            </template>
          </RowDivSlot>
          <RowDivSlot :label="'Информация'" :value="item['info']" />
          <RowDivSlot :label="'Иннициатор'" :value="item['initiator']" />
          <RowDivSlot :label="'Источник'" :value="item['source']" />
          <RowDivSlot :label="'Сотрудник'" :value="item['officer']" />
          <RowDivSlot :label="'Дата запроса'" :value="item['deadline']" />
        </CollapseDiv>
      </div>
      <p v-else>Данные отсутствуют</p>
      <div class="d-print-none py-3">
        <a
          class="btn btn-outline-primary"
          type="button"
          @click="
            need.isForm = true;
            need.action = 'create';
          "
          >Добавить запись
        </a>
      </div>
    </div>
  </div>
</template>
