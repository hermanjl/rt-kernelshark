#ifndef _RT_GRAPH_H
#define _RT_GRAPH_H

#include <gtk/gtk.h>
#include "trace-cmd.h"
#include "task-list.h"

struct rt_graph_info {

	/* List of all tasks */
	struct task_list 	*tasks[TASK_HASH_SIZE];

	/* Cache of event fields so that they don't need to be located
	 * during each access.
	 */
	gint 			task_param_id;
	struct format_field 	*param_pid_field;
	struct format_field 	*param_wcet_field;
	struct format_field 	*param_period_field;

	gint 			task_release_id;
	struct format_field 	*release_pid_field;
	struct format_field 	*release_job_field;
	struct format_field	*release_release_field;
	struct format_field 	*release_deadline_field;

	gint			task_completion_id;
	struct format_field 	*completion_pid_field;
	struct format_field 	*completion_job_field;
	struct format_field	*completion_when_field;

	gint 			task_block_id;
	struct format_field 	*block_pid_field;
	struct format_field	*block_when_field;

	gint 			task_resume_id;
	struct format_field 	*resume_pid_field;
	struct format_field	*resume_when_field;

};

/* Event parsers */
int rt_graph_check_task_param(struct rt_graph_info *rtinfo, struct pevent *pevent,
			      struct record *record, gint *pid,
			      unsigned long long *wcet,
			      unsigned long long *period);
int rt_graph_check_task_release(struct rt_graph_info *rtinfo, struct pevent *pevent,
				struct record *record, gint *pid, gint *job,
				unsigned long long *release,
				unsigned long long *deadline);
int rt_graph_check_task_completion(struct rt_graph_info *rtinfo, struct pevent *pevent,
				   struct record *record, gint *pid, gint *job,
				   unsigned long long *when);
int rt_graph_check_task_block(struct rt_graph_info *rtinfo, struct pevent *pevent,
			      struct record *record, gint *pid,
			      unsigned long long *when);
int rt_graph_check_task_resume(struct rt_graph_info *rtinfo, struct pevent *pevent,
			       struct record *record, gint *pid,
			       unsigned long long *when);
void init_rt_event_cache(struct rt_graph_info *rtinfo);

/* Metadata */
void rt_plot_task_plotted(struct rt_graph_info *rt_info, gint **plotted);

/* Callbacks for managing task list */
void rt_plot_task_update_callback(gboolean accept, gint *selected,
				  gint *non_select, gpointer data);
void rt_plot_task_plotted(struct rt_graph_info *rtinfo, gint **plotted);

#endif
