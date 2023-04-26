<template>
  <div class="tree-view">
    <ul>
      <li v-for="node in treeData" :key="node.id">
        {{ node.label }}
        <ul>
          <li v-for="child in node.children" :key="child.id">
            {{ child.label }}
            <ul>
              <li v-for="attribute in attributes" :key="attribute">
                {{ attribute }}: {{ child[attribute] }}
              </li>
            </ul>
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'TreeView',
  props: {
    treeData: {
      type: Array,
      default: () => []
    },
    attributes: {
      type: Array,
      default: () => []
    }
  }
}
</script>
