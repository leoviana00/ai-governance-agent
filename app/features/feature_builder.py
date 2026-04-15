def build_features(dataset):

    X = []
    y = []

    for d in dataset:

        metrics = d.get("change_metrics", {})
        governance = d.get("governance", {})

        # ----------------------------
        # valida registros incompletos
        # ----------------------------
        if (
            metrics.get("files_changed") is None or
            metrics.get("lines_added") is None or
            metrics.get("lines_removed") is None or
            metrics.get("modules_affected") is None or
            d.get("incident") is None
        ):
            continue

        # ----------------------------
        # FEATURES BASE
        # ----------------------------
        files_changed = int(metrics.get("files_changed", 0))
        lines_added = int(metrics.get("lines_added", 0))
        lines_removed = int(metrics.get("lines_removed", 0))
        modules_affected = int(metrics.get("modules_affected", 0))

        # ----------------------------
        # GOVERNANÇA
        # ----------------------------
        semantic_commit = 1 if governance.get("semantic_commit") else 0
        self_approved = 1 if governance.get("self_approved") else 0

        # ----------------------------
        # CHANGE TYPE
        # ----------------------------
        change_type = governance.get("change_type")

        is_feat = 1 if change_type == "feat" else 0
        is_fix = 1 if change_type == "fix" else 0
        is_refactor = 1 if change_type == "refactor" else 0

        # ----------------------------
        # BRANCH TYPE
        # ----------------------------
        branch_type = governance.get("branch_type")

        is_hotfix = 1 if branch_type == "hotfix" else 0
        is_feature_branch = 1 if branch_type == "feature" else 0

        # ----------------------------
        # VETOR FINAL (11 FEATURES)
        # ----------------------------
        features = [
            files_changed,
            lines_added,
            lines_removed,
            modules_affected,

            semantic_commit,
            self_approved,

            is_feat,
            is_fix,
            is_refactor,

            is_hotfix,
            is_feature_branch
        ]

        X.append(features)
        y.append(int(d["incident"]))

    return X, y