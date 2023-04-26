
import TreeView from './components/TreeView.vue'

export default {
  name: 'App',
  components: {
    TreeView
  },
  data () {
    return {
      treeData: [],
      attributes: ['attr1', 'attr2']
    }
  },
  async created1 () {
        const response = await fetch("/get_tree_data");
        const jsonData = await response.json()
        alert(jsonData);
    }
}
