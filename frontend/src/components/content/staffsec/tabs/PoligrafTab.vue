<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const RowDivSlot = defineAsyncComponent(
  () => import("@components/elements/RowDivSlot.vue")
);
const PoligrafForm = defineAsyncComponent(
  () => import("../forms/PoligrafForm.vue")
);
const FileForm = defineAsyncComponent(
  () => import("@components/layouts/HeaderDiv.vue")
);
const ModalWin = defineAsyncComponent(
  () => import("@components/layouts/ModalWin.vue")
);

const emit = defineEmits(["get-item", "delete", "submit", "file"]);

onBeforeMount(async () => {
  emit("get-item", "poligraf");
});

const props = defineProps({
  poligrafs: {
    type: Array as () => Array<Record<any, string>>,
    default: () => {},
  },
});

const poligraf = ref({
  action: "",
  itemId: "",
  item: <Record<any, string>>{},
});

function cancelEdit() {
  poligraf.value.action = "";
  poligraf.value.item = {};
}

function submitForm(form: Object) {
  emit("submit", [
    poligraf.value.action,
    "poligraf",
    poligraf.value.itemId,
    form,
  ]);
  cancelEdit();
}

function submitFile(event: Event) {
  emit("file", event);
}

function deleteItem(itemId: string) {
  emit("delete", [itemId, "poligraf"]);
}
</script>

<template>
  <div class="py-3">
    <ModalWin
      :title="
        poligraf.action === 'update' ? 'Изменить запись' : 'Добавить запись'
      "
      :id="'modalPfo'"
      @cancel="cancelEdit"
    >
      <PoligrafForm
        :content="poligraf.item"
        @submit="submitForm"
      />
    </ModalWin>
    <div v-if="props.poligrafs.length > 0">
      <CollapseDiv
        v-for="(item, idx) in props.poligrafs"
        :key="idx"
        :id="'poligraf' + idx.toString()"
        :idx="idx.toString()"
        :label="'Полиграф #' + (idx + 1).toString()"
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
              data-bs-toggle="modal"
              data-bs-target="#modalPfo"
              @click="
                poligraf.action = 'update';
                poligraf.item = item;
                poligraf.itemId = item['id'].toString();
              "
            >
              <i class="bi bi-pencil-square"></i>
            </a>
          </template>
        </RowDivSlot>
        <RowDivSlot :label="'Тема'" :value="item['theme']" />
        <RowDivSlot :label="'Результат'" :value="item['results']" />
        <RowDivSlot :label="'Сотрудник'" :value="item['officer']" />
        <RowDivSlot
          :label="'Дата'"
          :value="
            new Date(String(item['deadline'])).toLocaleDateString('ru-RU')
          "
        />
      </CollapseDiv>
      <FileForm :accept="'*'" @submit="submitFile" />
    </div>
    <p v-else>Данные отсутствуют</p>
    <div class="d-print-none py-3">
      <a
        class="btn btn-outline-primary"
        type="button"
        data-bs-toggle="modal"
        data-bs-target="#modalPfo"
        @click="poligraf.action = 'create'"
      >Добавить запись
      </a>
    </div>
  </div>
</template>
