<script setup lang="ts">
import { ref, defineAsyncComponent, onBeforeMount } from "vue";
import { Pfo } from "@/interfaces/interface";

const PoligrafForm = defineAsyncComponent(
  () => import("@components/forms/PoligrafForm.vue")
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
  poligrafs:  {
    type: Array as () => Pfo[],
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

const poligraf = ref({
  action: "",
  isForm: false,
  itemId: "",
  item: <Pfo>{},
});
</script>

<template>
  <div class="py-3">
    <template v-if="poligraf.isForm">
    <PoligrafForm
      :get-item="props.getItem"
      :action="poligraf.action"
      :cand-id="candId"
      :content="poligraf.item"
      :update-item="props.updateItem"
      @deactivate="poligraf.isForm = false; poligraf.action = '';"
    />
    </template>
    <div v-else>
      <div v-if="props.poligrafs.length > 0">
        <CollapseDiv
          v-for="(item, idx) in props.poligrafs"
          :key="idx"
          :id="'poligraf' + idx"
          :idx="idx"
          :label="'Полиграф #' + (idx + 1)"
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
                  poligraf.isForm = true;
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
            :value="new Date(String(item['deadline'])).toLocaleDateString('ru-RU')"
          />
          <RowDivSlot :slotOne="true" :print="true">
            <form
              class="form"
              enctype="multipart/form-data"
              role="form"
              @change="
                  props.submitFile(
                    $event,
                    item['id'].toString(),
                    'poligraf'
                )
              "
            >
              <input class="form-control" id="file" type="file" ref="file" multiple />
            </form>
          </RowDivSlot>
        </CollapseDiv>
      </div>
      <p v-else>Данные отсутствуют</p>
      <div class="d-print-none py-3">
        <a
          class="btn btn-outline-primary"
          type="button"
          @click="
            poligraf.isForm = true;
            poligraf.action = 'create';
          "
          >Добавить запись
        </a>
      </div>
    </div>
  </div>
</template>
