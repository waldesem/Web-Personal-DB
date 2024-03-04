<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
import { Needs } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);
const InquiryForm = defineAsyncComponent(
  () => import("../forms/InquiryForm.vue")
);

const emit = defineEmits(["get", "delete", "submit"]);

onBeforeMount( async() => {
  emit("get", "inquiry");
});

const props = defineProps({
  candId: String,
  needs:  {
    type: Array as () => Array<Needs>,
    default: () => [],
  },
});

const need = ref({
  action: "",
  itemId: "",
  isForm: false,
  item: <Needs>{},
});

function deactivateEmit() {
  need.value.isForm = false; 
  need.value.action = '';
};

function submitEmit(
  itemId: string, 
  form: Object
  ) {
  emit("submit", [need.value.action, "inquiry", itemId, form])
};

function deleteItem(itemId: string){
  emit("delete", [itemId, "inquiry"])
};
</script>

<template>
  <div class="py-3">
    <template v-if="need.isForm">
      <InquiryForm
        :cand-id="candId"
        :content="need.item"
        :action="need.action"
        @submit="submitEmit"
        @deactivate="deactivateEmit"
      />
    </template>
    <div v-else>
      <div v-if="props.needs.length">
        <CollapseDiv
          v-for="(item, idx) in props.needs"
          :key="idx"
          :id="'inquiry' + idx.toString()"
          :idx="idx.toString()"
          :label="'Запрос #' + (idx + 1).toString()"
        >
          <RowDivSlot :slotTwo="true" :print="true">
            <template v-slot:divTwo>
              <a
                href="#"
                title="Удалить"
                @click="deleteItem(item['id'].toString())"
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
