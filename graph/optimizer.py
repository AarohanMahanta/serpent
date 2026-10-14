from tensor.tensor import Tensor


class Optimizer:
    def __init__(self, graph):
        self.graph = graph

    def constant_fold(self):
        folded = 0
        for node_id, node in self.graph.nodes.items():
            if node.op == 'input':
                continue
            inputs = [
                self.graph.nodes[src]
                for src, dst in self.graph.edges
                if dst == node_id
            ]
            all_constant = all(n.op == 'input' for n in inputs)
            if all_constant:
                node.op = 'input'
                folded += 1
        return folded

    def dead_node_elimination(self):
        reachable = set()
        output_id = list(self.graph.nodes.keys())[0]

        def walk(node_id):
            if node_id in reachable:
                return
            reachable.add(node_id)
            for src, dst in self.graph.edges:
                if dst == node_id:
                    walk(src)

        walk(output_id)
        before = len(self.graph.nodes)
        self.graph.nodes = {k: v for k, v in self.graph.nodes.items() if k in reachable}
        self.graph.edges = [(s, d) for s, d in self.graph.edges if s in reachable and d in reachable]
        return before - len(self.graph.nodes)

    def optimize(self):
        folded = self.constant_fold()
        eliminated = self.dead_node_elimination()
        print(f"[optimizer] constant folding: {folded} nodes folded")
        print(f"[optimizer] dead node elimination: {eliminated} nodes removed")
        return self.graph

    def operator_fusion(self):
        fused = 0
        fuseable = {('mul', 'add'), ('add', 'tanh'), ('mul', 'tanh')}

        for src_id, dst_id in list(self.graph.edges):
            src = self.graph.nodes.get(src_id)
            dst = self.graph.nodes.get(dst_id)
            if src and dst and (src.op, dst.op) in fuseable:
                dst.op = f"fused_{src.op}_{dst.op}"
                src.op = 'eliminated'
                fused += 1

        self.graph.nodes = {
            k: v for k, v in self.graph.nodes.items()
            if v.op != 'eliminated'
        }
        return fused
    