import torch as th

# from ..utils.plotting import plot


class MimicIVExtractor(Flow):
    r"""
    Extraction flow for mimic-iv patient graphs
    """

    def __init__(self, args):
        """
        flow for extracting mimic-iv dataset
        """
        super(MimicIVExtractor, self).__init__(args)

        self.diag_level = self.conf["general"]["diag_level"]
        self.aux_relations = self.conf["general"]["aux_relations"]
        self.aux_features = self.conf["general"]["aux_features"]
        self.feature_scale = self.conf["general"]["feature_scale"]
        self.plot_aux_feats = self.conf["general"]["plot_aux_feats"]

    def run_flow(self):
        self.construct_graph()

        # Generate data split
        self.graph.add_data_split("S", 0.8, 0.1)
        self.gen_labels("S", "S-D")

        # Drop relations from graph
        self.graph.drop_relations([("S", "S-D", "D"), ("D", "D-S", "S")])

        # Add domain features to the graph
        self.add_aux_features()

        # Add extra information to graph
        self.graph.add_extra(self.diag_level, "diag_level")

        # Save Graph
        self.graph.save_graph(self.path["output_fold"])

    def construct_graph(self):
        # Extract from data source
        self.extract_entities()
        self.extract_relations()
        self.extract_features()

        # Construct entities and relations
        self.construct_entities()
        self.construct_relations()

        # The original entity ids are substituted by new ids starting
        # from 0. The relation maps are updated and index-maps are
        # kept for backwards compatability
        self.graph.reindex_graph()

        # Add auxiliary relations to the graph
        self.add_aux_relations()

        # Create dgl graph representation
        self.graph.create_graph()

        return self.graph.graph

    def add_aux_relations(self):
        if self.aux_relations:
            self.relation_constructor.construct_relations()
            self.graph.add_aux_relations(self.relation_constructor.relation_map)

    def add_aux_features(self):
        if self.aux_features:
            self.feature_constructor.construct_features(self.graph)
            features = self.feature_constructor.feature_map
            hrchys = self.feature_constructor.hrchys

            self.graph.add_aux_features(features)
            if self.feature_scale:
                self.graph.scale_features(features, self.feature_scale, hrchys)

            if self.plot_aux_feats:
                raise NotImplemented()
                # plot(features, hrchys)

    def gen_labels(self, ntype, etype):
        ...
