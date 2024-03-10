<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
import { Pfo } from "@/interfaces/interface";

const CollapseDiv = defineAsyncComponent(
  () => import("@components/elements/CollapseDiv.vue")
);
const LabelSlot = defineAsyncComponent(
  () => import("@components/elements/LabelSlot.vue")
);
const LabelValue = defineAsyncComponent(
  () => import("@components/elements/LabelValue.vue")
);
const PoligrafForm = defineAsyncComponent(
  () => import("../forms/PoligrafForm.vue")
);
const FileForm = defineAsyncComponent(
  () => import("@components/layouts/HeaderDiv.vue")
);

const emit = defineEmits(["get-item", "delete", "submit", "file"]);

onBeforeMount(async () => {
  emit("get-item", "poligraf");
});

const props = defineProps({
  poligrafs: {
    type: Array as () => Array<Pfo>,
    default: () => [],
  },
});

const poligraf = ref({
  action: "",
  itemId: "",
  item: <Pfo>{},
});

function submitForm(form: Object) {
  emit(
    "submit", 
    poligraf.value.action,
    "poligraf",
    poligraf.value.itemId,
    form,
  );
  poligraf.value.action = "";
}

function submitFile(event: Event) {
  emit("file", event);
};
</script>

<template>
  <div class="py-3">
    <PoligrafForm v-if="poligraf.action"
      :poligraf="poligraf.item"
      @submit="submitForm"
      @cancel="poligraf.action = ''"
    />
    <div v-else>
      <div v-if="props.poligrafs.length > 0">
        <CollapseDiv
          v-for="(item, idx) in props.poligrafs"
          :key="idx"
          :id="'poligraf' + idx"
          :idx="idx.toString()"
          :label="'Полиграф #' + (idx + 1)"
        >
          <LabelSlot>
            <a
              href="#"
              title="Удалить"
              @click="emit('delete', item['id'].toString(), 'poligraf')"
            >
              <i class="bi bi-trash"></i>
            </a>
            &nbsp;
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
          </LabelSlot>
          <LabelValue :label="'Тема'" :value="item['theme']" />
          <LabelValue :label="'Результат'" :value="item['results']" />
          <LabelValue :label="'Сотрудник'" :value="item['officer']" />
          <LabelValue
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
          @click="poligraf.action = 'create'"
        >Добавить запись
        </a>
      </div>
    </div>
  </div>
</template>
